from expert.models import Concept, Skill
from learner.models import LearnerProgress
from .llm_client import GeminiClient

class TutorService:
    def __init__(self, learner_profile):
        self.learner = learner_profile
        self.llm_client = GeminiClient()

    def _get_or_create_progress(self, concept):
        progress, created = LearnerProgress.objects.get_or_create(
            learner=self.learner,
            concept=concept
        )
        return progress

    def _determine_next_concept(self):
        """
        Logique simple pour choisir le prochain concept.
        Priorité 1: Concepts commencés mais non maîtrisés (score < 0.9).
        Priorité 2: Nouveaux concepts dans l'ordre de l'arbre.
        """
        # Chercher un concept en cours avec un faible score
        in_progress_concepts = LearnerProgress.objects.filter(
            learner=self.learner,
            mastery_score__lt=0.9
        ).order_by('last_interaction_at').first()

        if in_progress_concepts:
            return in_progress_concepts.concept

        # Sinon, trouver le premier concept jamais vu
        learned_concept_ids = LearnerProgress.objects.filter(learner=self.learner).values_list('concept_id', flat=True)
        
        # On prend le premier concept de l'arbre qui n'a pas été appris
        # Note: une vraie logique suivrait les dépendances de l'arbre MPTT
        next_concept = Concept.objects.exclude(id__in=learned_concept_ids).order_by('skill__tree_id', 'skill__lft', 'id').first()

        return next_concept

    def _build_prompt(self, concept, user_message, progress):
        """
        Construit le prompt pour le LLM. C'est la partie la plus créative !
        """
        # Récupérer un peu d'historique
        history = progress.interaction_history[-3:] # Les 3 dernières interactions

        prompt = f"""
        Tu es un tuteur intelligent, patient et encourageant. Ton nom est "Prof".
        Ton objectif est d'aider un apprenant à maîtriser un concept spécifique.

        **Règles strictes :**
        1.  Ne parle que du concept actuel. Ne dérive pas sur d'autres sujets.
        2.  Utilise un langage simple et des analogies.
        3.  Termine TOUJOURS ta réponse par une question simple pour vérifier la compréhension de l'apprenant.
        4.  Garde tes réponses courtes et directes (2-3 phrases maximum).

        ---
        **CONTEXTE DE L'APPRENANT**
        - Nom de l'apprenant : {self.learner.user.username}
        - Score de maîtrise actuel sur ce concept : {progress.mastery_score:.2f}

        **CONCEPT ACTUEL À ENSEIGNER**
        - Nom du concept : {concept.name}
        - Explication de base : {concept.explanation}

        **HISTORIQUE DE LA CONVERSATION (sur ce concept)**
        {history if history else "C'est notre première interaction sur ce sujet."}

        ---
        **DERNIER MESSAGE DE L'APPRENANT :**
        "{user_message}"
        ---
        
        Ta réponse (en tant que Prof, courte, simple, et se terminant par une question) :
        """
        return prompt.strip()

    def _update_progress(self, progress, user_message, tutor_response):
        """
        Met à jour le modèle de l'apprenant après l'interaction.
        Pour l'instant, on augmente simplement le score un peu à chaque interaction.
        Une vraie version analyserait la réponse de l'utilisateur.
        """
        progress.mastery_score = min(1.0, progress.mastery_score + 0.1) # Augmentation simpliste
        
        # Ajout à l'historique
        progress.interaction_history.append({
            "user": user_message,
            "tutor": tutor_response
        })
        
        progress.save()
        return progress

    def handle_interaction(self, user_message):
        """
        Point d'entrée principal du service. Orchestre le flux.
        """
        # 1. Décider sur quel concept travailler
        concept_to_teach = self._determine_next_concept()
        print(f"====== Concept to teach : {concept_to_teach} ==========")
        if not concept_to_teach:
            return {
                "tutor_response": "Félicitations ! Vous avez terminé tous les modules disponibles pour le moment.",
                "current_concept_name": "Terminé",
                "mastery_score": 1.0
            }

        # 2. Récupérer l'état de progression de l'apprenant sur ce concept
        progress = self._get_or_create_progress(concept_to_teach)

        effective_user_message = user_message
        if progress.mastery_score == 0.0:
            effective_user_message = "Commençons cette leçon."
        # --------------------

        prompt = self._build_prompt(concept_to_teach, effective_user_message, progress)
        tutor_response_text = self.llm_client.generate_response(prompt)

        updated_progress = self._update_progress(progress, user_message, tutor_response_text)

        return {
            "tutor_response": tutor_response_text,
            "current_concept_name": concept_to_teach.name,
            "mastery_score": updated_progress.mastery_score
        }
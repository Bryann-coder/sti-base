from .models import *
try:
    from .llm_client import GeminiClient
except ImportError:
    from .llm_mock import MockGeminiClient as GeminiClient
    print("⚠️  Utilisation du mock LLM (dépendances manquantes)")
import uuid
from django.utils import timezone
import json

class SystemeTuteur:
    def __init__(self):
        self.detecteur_erreur = DetecteurErreur()
        self.systeme_pedagogique = SystemePedagogique()
        self.gamification = Gamification.objects.first() or Gamification.objects.create(
            id_gamification="default"
        )
    
    def traiter_message(self, utilisateur, message, session=None):
        """Point d'entrée principal pour traiter un message utilisateur"""
        
        # Créer ou récupérer la session
        if not session:
            niveau = Niveau.objects.first()  # Simplification
            session = utilisateur.demarrer_session(niveau)
            session.id_session = str(uuid.uuid4())
            session.objectif_session = "Apprentissage du diagnostic médical"
            session.save()
        
        # Créer l'interaction
        interaction = Interaction.objects.create(
            id_interaction=str(uuid.uuid4()),
            message=message,
            type_message=TypeMessage.QUESTION,
            auteur=utilisateur.nom,
            timestamp=timezone.now()
        )
        
        # Détection d'erreurs
        erreurs_detectees = self.detecteur_erreur.analyser(message, session)
        if erreurs_detectees:
            interaction.contient_erreur = True
            interaction.erreurs_detectees.set(erreurs_detectees)
        
        # Récupération du profil et historique
        profil = utilisateur.profil
        historique_sessions = utilisateur.obtenir_historique()
        
        # Traitement pédagogique
        reponse = self.systeme_pedagogique.traiter_interaction(
            interaction, session, profil, historique_sessions
        )
        
        # Création de la réponse
        reponse_interaction = Interaction.objects.create(
            id_interaction=str(uuid.uuid4()),
            message=reponse['message'],
            type_message=TypeMessage.REPONSE,
            auteur="Système Tuteur",
            timestamp=timezone.now()
        )
        
        # Ajout des interactions à la session
        session.ajouter_interaction(interaction)
        session.ajouter_interaction(reponse_interaction)
        
        # Mise à jour du cache historique
        if not hasattr(session, 'historique_cache') or session.historique_cache is None:
            session.historique_cache = []
        
        session.historique_cache.extend([
            {
                'auteur': interaction.auteur,
                'message': interaction.message,
                'timestamp': interaction.timestamp.isoformat(),
                'type': interaction.type_message
            },
            {
                'auteur': reponse_interaction.auteur,
                'message': reponse_interaction.message,
                'timestamp': reponse_interaction.timestamp.isoformat(),
                'type': reponse_interaction.type_message
            }
        ])
        
        session.premiere_fois = False
        
        # Gestion de la fin de consultation
        fin_consultation = reponse.get('fin_consultation', False)
        diagnostic_correct = False
        
        if fin_consultation and reponse.get('diagnostic_propose'):
            session.diagnostic_propose = reponse['diagnostic_propose']
            diagnostic_correct = session.cas_clinique.verifier_diagnostic(reponse['diagnostic_propose']) if session.cas_clinique else False
        
        # Attribution d'étoiles
        etoiles = self.gamification.calculer_etoiles({'score': 4 if not erreurs_detectees else 2})
        session.score_etoiles += etoiles
        session.save()
        
        # Si fin de consultation, terminer la session
        if fin_consultation:
            session.terminer_session()
        
        return {
            'reponse': reponse['message'],
            'etoiles_gagnees': etoiles,
            'score_total': session.score_etoiles,
            'cas_clinique': session.cas_clinique.titre if session.cas_clinique else None,
            'fin_consultation': fin_consultation,
            'diagnostic_correct': diagnostic_correct,
            'feedback_pedagogique': reponse.get('feedback_pedagogique', '')
        }

class DetecteurErreur:
    def __init__(self):
        self.modele_ia = GeminiClient()
    
    def analyser(self, message, session):
        """Analyse le message pour détecter des erreurs ou difficultés"""
        
        # Prompt pour la détection d'erreurs
        prompt = f"""
        Analysez ce message d'un étudiant en médecine et identifiez les erreurs ou difficultés:
        
        Message: "{message}"
        Contexte: Session d'apprentissage médical
        
        Répondez uniquement par "AUCUNE_ERREUR" ou listez les types d'erreurs détectées séparées par des virgules.
        Types possibles: DIAGNOSTIC_INCORRECT, SYMPTOME_MANQUE, RAISONNEMENT_FLOU, TERMINOLOGIE_INCORRECTE
        """
        
        reponse_ia = self.modele_ia.generate_response(prompt)
        
        if "AUCUNE_ERREUR" in reponse_ia:
            return []
        
        # Créer des objets Erreur pour chaque type détecté
        erreurs = []
        types_erreurs = reponse_ia.split(',')
        
        for type_erreur in types_erreurs:
            type_erreur = type_erreur.strip()
            if type_erreur:
                erreur = Erreur.objects.create(
                    id_erreur=str(uuid.uuid4()),
                    type_erreur=type_erreur,
                    description=f"Erreur détectée: {type_erreur}",
                    contexte=message,
                    gravite="MOYENNE",
                    suggestion_correction="Réviser les concepts de base"
                )
                erreurs.append(erreur)
        
        return erreurs

class SystemePedagogique:
    def __init__(self):
        self.selecteur_cas = SelecteurCas()
        self.strategie = StrategiePedagogique.objects.first() or StrategiePedagogique.objects.create(
            id_strategie="default",
            nom="Stratégie Adaptative",
            type_approche="SOCRATIQUE"
        )
    
    def traiter_interaction(self, interaction, session, profil, historique):
        """Traite l'interaction et génère une réponse pédagogique"""
        
        # Sélection ou mise à jour du cas clinique
        if not session.cas_clinique or interaction.contient_erreur:
            cas_clinique = self.selecteur_cas.selectionner(profil, historique, session.etape)
            session.cas_clinique = cas_clinique
            session.save()
        
        # Génération de la réponse
        reponse = self.generer_reponse(interaction, session)
        
        return {
            'message': reponse,
            'evaluation': {'score': 3}  # Score simplifié
        }
    
    def generer_reponse(self, interaction, session):
        """Génère une réponse du système tuteur (patient virtuel + pédagogie)"""
        
        cas = session.cas_clinique
        historique = session.historique_cache if hasattr(session, 'historique_cache') else []
        profil = session.utilisateur.profil
        
        # Détecter si c'est une fin de consultation
        fin_consultation = self._detecter_fin_consultation(interaction.message)
        diagnostic_propose = self._extraire_diagnostic(interaction.message) if fin_consultation else None
        
        # Construction du contexte complet pour l'IA
        contexte_historique = self._formater_historique(historique)
        
        prompt = f"""
        Tu es un SYSTÈME TUTEUR INTELLIGENT qui simule un patient ET guide l'apprentissage.
        
        CONTEXTE DU CAS:
        - Patient: {cas.titre if cas else 'Patient général'}
        - Symptômes réels: {cas.symptomes if cas else 'Symptômes généraux'}
        - Diagnostic correct: {cas.diagnostic_correct if cas else 'Non défini'}
        - État mental: {cas.etat_mental_patient if cas else 'Coopératif'}
        
        PROFIL APPRENANT:
        - Niveau: {profil.niveau_expertise}
        - Spécialité: {profil.specialite}
        
        HISTORIQUE CONSULTATION:
        {contexte_historique}
        
        QUESTION/ACTION MÉDECIN: "{interaction.message}"
        
        INSTRUCTIONS:
        1. Si c'est une question médicale normale:
           - Réponds comme le PATIENT avec les symptômes du cas
           - Ajoute des conseils pédagogiques discrets
           - Guide vers les bonnes questions si nécessaire
        
        2. Si c'est un diagnostic ou une conclusion:
           - Évalue la justesse du diagnostic
           - Donne un feedback pédagogique détaillé
           - Explique les points forts et à améliorer
        
        3. Si c'est une erreur médicale:
           - Corrige avec bienveillance
           - Explique pourquoi c'est incorrect
           - Propose la bonne approche
        
        Réponds de manière naturelle et pédagogique.
        """
        
        client = GeminiClient()
        reponse = client.generate_response(prompt)
        
        return {
            'message': reponse,
            'fin_consultation': fin_consultation,
            'diagnostic_propose': diagnostic_propose
        }
    
    def _detecter_fin_consultation(self, message):
        """Détecte si le médecin termine la consultation"""
        mots_cles_fin = [
            'diagnostic', 'conclusion', 'prescription', 'traitement',
            'au revoir', 'merci', 'terminé', 'fini', 'ordonnance',
            'je pense que', 'mon diagnostic', 'je conclus'
        ]
        
        message_lower = message.lower()
        return any(mot in message_lower for mot in mots_cles_fin)
    
    def _extraire_diagnostic(self, message):
        """Extrait le diagnostic proposé par le médecin"""
        # Logique simple d'extraction
        message_lower = message.lower()
        if 'grippe' in message_lower:
            return 'Grippe'
        elif 'infarctus' in message_lower:
            return 'Infarctus du myocarde'
        elif 'angine' in message_lower:
            return 'Angine de poitrine'
        # Ajouter d'autres diagnostics courants
        return message  # Retourner le message complet si pas de correspondance
    
    def _formater_historique(self, historique):
        """Formate l'historique pour le prompt"""
        if not historique:
            return "Début de consultation"
        
        historique_str = ""
        for interaction in historique[-5:]:  # 5 dernières interactions
            historique_str += f"{interaction.get('auteur', 'Inconnu')}: {interaction.get('message', '')}\n"
        
        return historique_str

class SelecteurCas:
    def __init__(self):
        self.modele_ia = GeminiClient()
    
    def selectionner(self, profil, historique, etape):
        """Sélectionne un cas clinique adapté au profil de l'utilisateur"""
        
        # Récupérer les cas disponibles
        cas_disponibles = CasClinique.objects.all()
        
        if not cas_disponibles:
            # Créer un cas par défaut si aucun n'existe
            cas_defaut = CasClinique.objects.create(
                id_cas="cas_001",
                titre="Consultation de routine",
                description="Patient présentant des symptômes généraux",
                contexte_clinique="Consultation en médecine générale",
                diagnostic_correct="Syndrome grippal",
                niveau_difficulte="FACILE",
                etat_mental_patient="Patient coopératif et anxieux"
            )
            return cas_defaut
        
        # Sélection basée sur le niveau d'expertise
        niveau_expertise = profil.niveau_expertise.upper()
        
        if niveau_expertise == "DEBUTANT":
            cas_filtre = cas_disponibles.filter(niveau_difficulte="FACILE")
        elif niveau_expertise == "INTERMEDIAIRE":
            cas_filtre = cas_disponibles.filter(niveau_difficulte="MOYEN")
        else:
            cas_filtre = cas_disponibles.filter(niveau_difficulte="DIFFICILE")
        
        if not cas_filtre:
            cas_filtre = cas_disponibles
        
        return cas_filtre.first()

class GestionSession:
    @staticmethod
    def creer_session(utilisateur, niveau_id, etape_id=None):
        """Crée une nouvelle session d'apprentissage"""
        
        niveau = Niveau.objects.get(id_niveau=niveau_id)
        etape = None
        if etape_id:
            etape = Etape.objects.get(id_etape=etape_id)
        
        session = Session.objects.create(
            id_session=str(uuid.uuid4()),
            utilisateur=utilisateur,
            niveau=niveau,
            etape=etape,
            objectif_session="Maîtriser les concepts du niveau",
            premiere_fois=True
        )
        
        return session
    
    @staticmethod
    def terminer_session(session):
        """Termine une session et calcule les résultats"""
        
        session.terminer_session()
        
        # Mise à jour de l'historique utilisateur
        historique, created = HistoriqueSession.objects.get_or_create(
            utilisateur=session.utilisateur,
            defaults={'id_historique': str(uuid.uuid4())}
        )
        
        historique.ajouter_resultat(session)
        historique.derniere_activite = timezone.now()
        historique.save()
        
        return session
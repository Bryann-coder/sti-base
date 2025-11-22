from .models import *
from .llm_client import GeminiClient
import uuid
from django.utils import timezone

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
        session.premiere_fois = False
        session.save()
        
        # Attribution d'étoiles
        etoiles = self.gamification.calculer_etoiles(reponse.get('evaluation', {}))
        session.score_etoiles += etoiles
        session.save()
        
        return {
            'reponse': reponse['message'],
            'etoiles_gagnees': etoiles,
            'score_total': session.score_etoiles,
            'cas_clinique': session.cas_clinique.titre if session.cas_clinique else None
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
        """Génère une réponse pédagogique adaptée"""
        
        cas = session.cas_clinique
        historique = session.obtenir_historique_session()
        
        # Construction du contexte pour l'IA
        contexte_historique = ""
        for inter in historique[-3:]:  # 3 dernières interactions
            contexte_historique += f"{inter.auteur}: {inter.message}\n"
        
        prompt = f"""
        Tu es un tuteur médical intelligent. Voici le contexte:
        
        CAS CLINIQUE:
        - Titre: {cas.titre if cas else 'Cas général'}
        - Description: {cas.description if cas else 'Formation générale'}
        - État mental du patient: {cas.etat_mental_patient if cas else 'Stable'}
        
        HISTORIQUE RÉCENT:
        {contexte_historique}
        
        MESSAGE ÉTUDIANT: {interaction.message}
        
        Réponds comme un tuteur bienveillant qui guide l'étudiant vers la bonne réponse.
        Termine par une question pour vérifier sa compréhension.
        Reste dans le contexte médical et du cas clinique.
        """
        
        client = GeminiClient()
        return client.generate_response(prompt)

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
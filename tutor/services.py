from .models import *
from .tuteur_service import SystemeTuteur, GestionSession
from django.contrib.auth.models import User
import uuid

class TutorService:
    def __init__(self, user):
        self.user = user
        self.utilisateur = self._get_or_create_utilisateur()
        self.systeme_tuteur = SystemeTuteur()
    
    def _get_or_create_utilisateur(self):
        """Récupère ou crée l'utilisateur du système tuteur"""
        try:
            return Utilisateur.objects.get(user=self.user)
        except Utilisateur.DoesNotExist:
            # Créer le profil utilisateur
            profil = ProfilUtilisateur.objects.create(
                id_profil=str(uuid.uuid4()),
                specialite="Médecine Générale",
                niveau_expertise="DEBUTANT",
                niveau_app="1",
                domaine="Santé"
            )
            
            # Créer l'utilisateur
            utilisateur = Utilisateur.objects.create(
                id_utilisateur=str(uuid.uuid4()),
                user=self.user,
                nom=self.user.last_name or "Utilisateur",
                prenom=self.user.first_name or "Nouveau",
                email=self.user.email,
                profil=profil
            )
            return utilisateur
    
    def handle_interaction(self, user_message, session_id=None):
        """Point d'entrée principal pour gérer une interaction"""
        
        # Récupérer ou créer la session
        session = None
        if session_id:
            try:
                session = Session.objects.get(id_session=session_id, utilisateur=self.utilisateur)
            except Session.DoesNotExist:
                pass
        
        # Si pas de session, en créer une nouvelle
        if not session:
            niveau = self._get_or_create_niveau_defaut()
            session = GestionSession.creer_session(self.utilisateur, niveau.id_niveau)
        
        # Traiter le message avec le système tuteur
        resultat = self.systeme_tuteur.traiter_message(self.utilisateur, user_message, session)
        
        return {
            "tutor_response": resultat['reponse'],
            "session_id": session.id_session,
            "etoiles_gagnees": resultat['etoiles_gagnees'],
            "score_total": resultat['score_total'],
            "cas_clinique": resultat['cas_clinique'],
            "niveau_actuel": session.niveau.nom
        }
    
    def _get_or_create_niveau_defaut(self):
        """Crée ou récupère le niveau par défaut"""
        niveau, created = Niveau.objects.get_or_create(
            id_niveau="niveau_1",
            defaults={
                "nom": "Niveau 1 - Bases du diagnostic",
                "description": "Apprentissage des bases du diagnostic médical",
                "ordre": 1,
                "nombre_etoiles_minimum": 20
            }
        )
        
        if created:
            # Créer des étapes pour ce niveau
            for i in range(1, 6):
                Etape.objects.create(
                    id_etape=f"etape_{i}",
                    niveau=niveau,
                    nom=f"Étape {i}",
                    description=f"Description de l'étape {i}",
                    ordre=i,
                    nombre_etoiles_max=5
                )
        
        return niveau
    
    def get_progression(self):
        """Récupère la progression de l'utilisateur"""
        sessions = self.utilisateur.obtenir_historique()
        total_etoiles = sum(session.score_etoiles for session in sessions)
        
        return {
            "total_etoiles": total_etoiles,
            "sessions_completees": sessions.filter(etat_session='TERMINEE').count(),
            "niveau_actuel": sessions.first().niveau.nom if sessions.exists() else "Aucun"
        }
    
    def terminer_session(self, session_id):
        """Termine une session"""
        try:
            session = Session.objects.get(id_session=session_id, utilisateur=self.utilisateur)
            GestionSession.terminer_session(session)
            return True
        except Session.DoesNotExist:
            return False
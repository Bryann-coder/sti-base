"""
Gestionnaire de sessions pour le système tuteur
Gère l'historique, le cache et les étapes de consultation
"""

from .models import *
from .llm_client import GeminiClient
import uuid
from django.utils import timezone

class SessionManager:
    def __init__(self, utilisateur):
        self.utilisateur = utilisateur
        self.llm_client = GeminiClient()
    
    def demarrer_nouvelle_session(self, niveau_id=None, etape_id=None):
        """Démarre une nouvelle session de consultation"""
        
        # Récupérer l'historique complet
        historique = self._recuperer_historique_complet()
        
        # Sélectionner niveau et étape
        niveau = self._selectionner_niveau(niveau_id)
        etape = self._selectionner_etape(etape_id, niveau)
        
        # Sélectionner cas clinique adapté
        cas_clinique = self._selectionner_cas_clinique(historique)
        
        # Créer la session
        session = Session.objects.create(
            id_session=str(uuid.uuid4()),
            utilisateur=self.utilisateur,
            niveau=niveau,
            etape=etape,
            cas_clinique=cas_clinique,
            objectif_session=f"Consultation: {cas_clinique.titre}",
            premiere_fois=True,
            historique_cache=historique
        )
        
        return session
    
    def reprendre_session(self, session_id):
        """Reprend une session existante avec son historique"""
        try:
            session = Session.objects.get(
                id_session=session_id, 
                utilisateur=self.utilisateur,
                etat_session='ACTIVE'
            )
            
            # Mettre à jour le cache avec l'historique récent
            historique_recent = self._recuperer_historique_session(session)
            session.historique_cache.extend(historique_recent)
            session.save()
            
            return session
        except Session.DoesNotExist:
            return None
    
    def _recuperer_historique_complet(self):
        """Récupère l'historique complet de l'utilisateur"""
        historique, created = HistoriqueSession.objects.get_or_create(
            utilisateur=self.utilisateur,
            defaults={'id_historique': str(uuid.uuid4())}
        )
        return historique.obtenir_historique_complet()
    
    def _recuperer_historique_session(self, session):
        """Récupère l'historique d'une session spécifique"""
        interactions = session.obtenir_historique_session()
        return [
            {
                'auteur': inter.auteur,
                'message': inter.message,
                'timestamp': inter.timestamp.isoformat(),
                'type': inter.type_message
            }
            for inter in interactions
        ]
    
    def _selectionner_niveau(self, niveau_id):
        """Sélectionne le niveau approprié"""
        if niveau_id:
            return Niveau.objects.get(id_niveau=niveau_id)
        
        # Niveau par défaut basé sur l'expertise
        expertise = self.utilisateur.profil.niveau_expertise
        if expertise == "DEBUTANT":
            niveau, _ = Niveau.objects.get_or_create(
                id_niveau="niveau_debutant",
                defaults={
                    'nom': "Consultations de base",
                    'description': "Apprentissage des consultations médicales de base",
                    'ordre': 1
                }
            )
        else:
            niveau, _ = Niveau.objects.get_or_create(
                id_niveau="niveau_avance",
                defaults={
                    'nom': "Consultations avancées", 
                    'description': "Cas complexes et diagnostics différentiels",
                    'ordre': 2
                }
            )
        return niveau
    
    def _selectionner_etape(self, etape_id, niveau):
        """Sélectionne l'étape appropriée"""
        if etape_id:
            return Etape.objects.get(id_etape=etape_id)
        
        # Étape par défaut
        etape, _ = Etape.objects.get_or_create(
            id_etape=f"etape_{niveau.id_niveau}",
            defaults={
                'niveau': niveau,
                'nom': "Consultation standard",
                'description': "Mener une consultation médicale complète",
                'ordre': 1
            }
        )
        return etape
    
    def _selectionner_cas_clinique(self, historique):
        """Sélectionne un cas clinique adapté en évitant les répétitions"""
        
        # Récupérer les cas déjà traités
        cas_traites = [h.get('cas_clinique') for h in historique if h.get('cas_clinique')]
        
        # Filtrer par niveau d'expertise
        expertise = self.utilisateur.profil.niveau_expertise
        difficulte_map = {
            'DEBUTANT': 'FACILE',
            'INTERMEDIAIRE': 'MOYEN', 
            'EXPERT': 'DIFFICILE'
        }
        
        cas_disponibles = CasClinique.objects.filter(
            niveau_difficulte=difficulte_map.get(expertise, 'FACILE')
        ).exclude(titre__in=cas_traites)
        
        if not cas_disponibles:
            cas_disponibles = CasClinique.objects.all()
        
        if not cas_disponibles:
            # Créer un cas par défaut
            return self._creer_cas_defaut()
        
        return cas_disponibles.first()
    
    def _creer_cas_defaut(self):
        """Crée un cas clinique par défaut"""
        return CasClinique.objects.create(
            id_cas=f"cas_defaut_{uuid.uuid4().hex[:8]}",
            titre="Patient avec symptômes généraux",
            description="Un patient se présente avec des symptômes non spécifiques",
            contexte_clinique="Consultation en médecine générale",
            symptomes={
                "principaux": ["fatigue", "maux de tête"],
                "secondaires": ["troubles du sommeil"]
            },
            diagnostic_correct="Syndrome de fatigue chronique",
            diagnostics_differentiels=["Dépression", "Hypothyroïdie", "Anémie"],
            niveau_difficulte="FACILE",
            etat_mental_patient="Patient coopératif mais inquiet"
        )
    
    def mettre_a_jour_cache(self, session, nouvelle_interaction):
        """Met à jour le cache de la session avec une nouvelle interaction"""
        session.historique_cache.append({
            'auteur': nouvelle_interaction.auteur,
            'message': nouvelle_interaction.message,
            'timestamp': nouvelle_interaction.timestamp.isoformat(),
            'type': nouvelle_interaction.type_message
        })
        session.save()
    
    def terminer_session(self, session, diagnostic_final=None):
        """Termine une session et met à jour l'historique global"""
        
        session.diagnostic_propose = diagnostic_final or ""
        session.terminer_session()
        
        # Mettre à jour l'historique global
        historique, _ = HistoriqueSession.objects.get_or_create(
            utilisateur=self.utilisateur,
            defaults={'id_historique': str(uuid.uuid4())}
        )
        
        historique.ajouter_resultat(session)
        historique.historique_complet.extend(session.historique_cache)
        historique.derniere_activite = timezone.now()
        historique.save()
        
        return session
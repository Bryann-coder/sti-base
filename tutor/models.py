from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class TypeMessage(models.TextChoices):
    QUESTION = 'QUESTION', 'Question'
    REPONSE = 'REPONSE', 'Réponse'
    CORRECTION = 'CORRECTION', 'Correction'
    FEEDBACK = 'FEEDBACK', 'Feedback'
    SYSTEME = 'SYSTEME', 'Système'

class ProfilUtilisateur(models.Model):
    id_profil = models.CharField(max_length=50, primary_key=True)
    specialite = models.CharField(max_length=100)
    niveau_expertise = models.CharField(max_length=50)
    niveau_app = models.CharField(max_length=50)
    domaine = models.CharField(max_length=100)
    competences = models.JSONField(default=list)
    performance_par_domaine = models.JSONField(default=dict)
    
    def mettre_a_jour_profil(self):
        self.save()
    
    def calculer_niveau_global(self):
        if not self.performance_par_domaine:
            return 0.0
        return sum(self.performance_par_domaine.values()) / len(self.performance_par_domaine)

class Utilisateur(models.Model):
    id_utilisateur = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    profil = models.OneToOneField(ProfilUtilisateur, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(default=timezone.now)
    
    def demarrer_session(self, niveau):
        return Session.objects.create(
            utilisateur=self,
            niveau=niveau,
            premiere_fois=True
        )
    
    def obtenir_historique(self):
        return self.sessions.all().order_by('-date_debut')

class Niveau(models.Model):
    id_niveau = models.CharField(max_length=50, primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    ordre = models.IntegerField()
    nombre_etoiles_minimum = models.IntegerField(default=20)
    test_final_actif = models.BooleanField(default=True)
    
    def verifier_conditions_passage(self, etoiles_utilisateur):
        return etoiles_utilisateur >= self.nombre_etoiles_minimum
    
    def obtenir_etapes_disponibles(self):
        return self.etapes.all()

class Etape(models.Model):
    id_etape = models.CharField(max_length=50, primary_key=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='etapes')
    nom = models.CharField(max_length=100)
    description = models.TextField()
    ordre = models.IntegerField()
    nombre_etoiles_max = models.IntegerField(default=5)
    obligatoire = models.BooleanField(default=False)
    prerequis = models.JSONField(default=list)
    
    def est_accessible(self, utilisateur):
        return True
    
    def calculer_progression(self, session):
        return session.score_etoiles / self.nombre_etoiles_max

class CasClinique(models.Model):
    id_cas = models.CharField(max_length=50, primary_key=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    contexte_clinique = models.TextField()
    symptomes = models.JSONField(default=dict)
    diagnostic_correct = models.CharField(max_length=200)
    diagnostics_differentiels = models.JSONField(default=list)
    niveau_difficulte = models.CharField(max_length=50)
    etat_mental_patient = models.TextField()
    
    def generer_presentation(self):
        return f"{self.titre}: {self.description}"
    
    def verifier_diagnostic(self, diagnostic_propose):
        return diagnostic_propose.lower() == self.diagnostic_correct.lower()
    
    def obtenir_indices(self, niveau_indice):
        return []

class Erreur(models.Model):
    id_erreur = models.CharField(max_length=50, primary_key=True)
    type_erreur = models.CharField(max_length=100)
    description = models.TextField()
    contexte = models.TextField()
    gravite = models.CharField(max_length=50)
    suggestion_correction = models.TextField()
    corrigee = models.BooleanField(default=False)
    
    def generer_feedback(self):
        return f"Erreur: {self.description}. Suggestion: {self.suggestion_correction}"

class Interaction(models.Model):
    id_interaction = models.CharField(max_length=50, primary_key=True)
    message = models.TextField()
    type_message = models.CharField(max_length=20, choices=TypeMessage.choices)
    timestamp = models.DateTimeField(default=timezone.now)
    auteur = models.CharField(max_length=100)
    contient_erreur = models.BooleanField(default=False)
    erreurs_detectees = models.ManyToManyField(Erreur, blank=True)
    
    def enregistrer(self):
        self.save()

class Session(models.Model):
    id_session = models.CharField(max_length=50, primary_key=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='sessions')
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    etape = models.ForeignKey(Etape, on_delete=models.CASCADE, null=True, blank=True)
    cas_clinique = models.ForeignKey(CasClinique, on_delete=models.CASCADE, null=True, blank=True)
    date_debut = models.DateTimeField(default=timezone.now)
    date_fin = models.DateTimeField(null=True, blank=True)
    score_etoiles = models.IntegerField(default=0)
    etat_session = models.CharField(max_length=50, default='ACTIVE')
    objectif_session = models.TextField()
    premiere_fois = models.BooleanField(default=True)
    interactions = models.ManyToManyField(Interaction, blank=True)
    
    def ajouter_interaction(self, interaction):
        self.interactions.add(interaction)
    
    def calculer_score(self):
        return self.score_etoiles
    
    def terminer_session(self):
        self.date_fin = timezone.now()
        self.etat_session = 'TERMINEE'
        self.save()
    
    def obtenir_historique_session(self):
        return self.interactions.all().order_by('timestamp')

class StrategiePedagogique(models.Model):
    id_strategie = models.CharField(max_length=50, primary_key=True)
    nom = models.CharField(max_length=100)
    type_approche = models.CharField(max_length=100)
    parametres = models.JSONField(default=dict)
    niveau_adaptation = models.IntegerField(default=1)
    
    def appliquer(self, interaction, cas_clinique):
        return "Réponse adaptée"
    
    def generer_feedback(self, resultat_evaluation):
        return "Feedback généré"

class Gamification(models.Model):
    id_gamification = models.CharField(max_length=50, primary_key=True)
    points_par_etape = models.JSONField(default=dict)
    seuil_passage_niveau = models.IntegerField(default=20)
    recompenses = models.JSONField(default=dict)
    
    def calculer_etoiles(self, resultat_evaluation):
        return min(5, max(1, resultat_evaluation.get('score', 0)))
    
    def verifier_deblocage_niveau(self, utilisateur, niveau):
        progression = getattr(utilisateur, 'progression', None)
        if progression:
            return progression.etoiles_niveau >= self.seuil_passage_niveau
        return False

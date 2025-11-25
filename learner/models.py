from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from expert.models import Concept

class LearnerProfile(models.Model):
    """
    Correspond à la classe 'ProfilUtilisateur' du diagramme.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learnerprofile')
    
    # Champs du diagramme ProfilUtilisateur
    specialite = models.CharField(max_length=100, blank=True, null=True)
    niveau_expertise = models.CharField(max_length=50, blank=True, null=True) # Ex: Débutant, Intermédiaire
    niveau_app = models.CharField(max_length=50, blank=True, null=True)       # Niveau dans l'application
    domaine = models.CharField(max_length=100, blank=True, null=True)         # Ex: Informatique, Mathématiques
    
    # performanceParDomaine (Map<String, Float>) -> JSONField en Django
    performance_par_domaine = models.JSONField(default=dict, blank=True)

    # Note: La liste 'competences' est implicitement gérée par le modèle LearnerProgress 
    # qui lie le profil aux Concepts/Skills.

    def mettre_a_jour_profil(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def calculer_niveau_global(self):
        # Logique simplifiée pour l'exemple
        if not self.performance_par_domaine:
            return 0.0
        scores = self.performance_par_domaine.values()
        return sum(scores) / len(scores)

    def __str__(self):
        return f"Profil de {self.user.username}"

class LearnerProgress(models.Model):
    """
    Table pivot qui suit la maîtrise d'un apprenant pour un concept donné.
    """
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    mastery_score = models.FloatField(default=0.0, help_text="Score de 0.0 (non vu) à 1.0 (maîtrisé).")
    last_interaction_at = models.DateTimeField(default=timezone.now)
    interaction_history = models.JSONField(default=list, help_text="Liste des interactions (questions/réponses).")

    class Meta:
        unique_together = ('learner', 'concept')

    def __str__(self):
        return f"{self.learner.user.username}'s progress on {self.concept.name}"
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from expert.models import Concept

class LearnerProfile(models.Model):
    """
    Extension du modèle User de base pour ajouter des informations spécifiques.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # On pourrait ajouter ici : avatar, bio, objectifs...

    def __str__(self):
        return self.user.username

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
        unique_together = ('learner', 'concept') # Un seul enregistrement par apprenant et par concept

    def __str__(self):
        return f"{self.learner.user.username}'s progress on {self.concept.name}"
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import LearnerProfile

@receiver(post_save, sender=User)
def create_learner_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement un LearnerProfile chaque fois qu'un nouvel User est créé.
    """
    if created:
        LearnerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_learner_profile(sender, instance, **kwargs):
    """
    Sauvegarde le profil associé à l'utilisateur.
    """
    instance.learnerprofile.save()
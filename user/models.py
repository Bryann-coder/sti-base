from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100, default="Médecine Générale")
    niveau_expertise = models.CharField(max_length=50, default="DEBUTANT")
    niveau_app = models.CharField(max_length=50, default="1")
    domaine = models.CharField(max_length=100, default="Santé")
    date_creation = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.specialite}"
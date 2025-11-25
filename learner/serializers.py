from rest_framework import serializers
from django.contrib.auth.models import User
from .models import LearnerProfile
from django.db import transaction

# --- Serializers existants ---
class InteractionInputSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)

class InteractionOutputSerializer(serializers.Serializer):
    tutor_response = serializers.CharField()
    current_concept_name = serializers.CharField()
    mastery_score = serializers.FloatField()

# --- Nouveaux Serializers pour l'Authentification ---

class RegisterSerializer(serializers.ModelSerializer):
    # Champs pour User
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)  # Prénom
    last_name = serializers.CharField(required=True)   # Nom
    email = serializers.EmailField(required=True)

    # Champs pour LearnerProfile (optionnels à l'inscription)
    specialite = serializers.CharField(required=False, allow_blank=True)
    domaine = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'specialite', 'domaine')

    def create(self, validated_data):
        # On extrait les données du profil
        specialite = validated_data.pop('specialite', '')
        domaine = validated_data.pop('domaine', '')
        
        # On utilise une transaction atomique pour s'assurer que tout est créé ou rien
        with transaction.atomic():
            # 1. Création de l'utilisateur standard Django
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )

            # 2. Le signal create_learner_profile (dans signals.py) a déjà créé un profil vide.
            # On le récupère et on le met à jour.
            profile = user.learnerprofile
            profile.specialite = specialite
            profile.domaine = domaine
            profile.save()

            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
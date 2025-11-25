from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    specialite = serializers.CharField(required=False, default="Médecine Générale")
    niveau_expertise = serializers.CharField(required=False, default="DEBUTANT")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'specialite', 'niveau_expertise']
    
    def create(self, validated_data):
        specialite = validated_data.pop('specialite', 'Médecine Générale')
        niveau_expertise = validated_data.pop('niveau_expertise', 'DEBUTANT')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        
        UserProfile.objects.create(
            user=user,
            specialite=specialite,
            niveau_expertise=niveau_expertise
        )
        
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'specialite', 'niveau_expertise', 'domaine', 'date_creation']
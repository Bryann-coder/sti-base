from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

from .serializers import (
    InteractionInputSerializer, 
    InteractionOutputSerializer, 
    RegisterSerializer, 
    LoginSerializer
)
from .models import LearnerProfile
from tutor.services import TutorService

# --- Vue d'Inscription ---
class RegisterView(APIView):
    permission_classes = [AllowAny] # Tout le monde peut s'inscrire

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Vue de Connexion ---
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request=request, username=username, password=password)

            if user:
                # C'est cette ligne qui crée la session (cookie)
                login(request, user)
                
                return Response({
                    "message": "Connexion réussie.",
                    "user_id": user.pk,
                    "username": user.username,
                    "nom": user.last_name,
                    "prenom": user.first_name,
                    "specialite": getattr(user.learnerprofile, 'specialite', '')
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Identifiants invalides"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Vue existante (Interaction Tuteur) ---
class TutorInteractionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 1. Valider l'entrée de l'utilisateur
        input_serializer = InteractionInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Récupérer le profil
        try:
            learner_profile = LearnerProfile.objects.get(user=request.user)
        except LearnerProfile.DoesNotExist:
            return Response({"error": "Profil introuvable"}, status=status.HTTP_404_NOT_FOUND)

        # 3. Service Tuteur
        user_message = input_serializer.validated_data['message']
        tutor_service = TutorService(learner_profile)
        response_data = tutor_service.handle_interaction(user_message)

        # 4. Réponse
        output_serializer = InteractionOutputSerializer(response_data)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)
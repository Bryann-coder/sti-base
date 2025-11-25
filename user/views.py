from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import UserProfile

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'Utilisateur créé avec succès',
            'user_id': user.id,
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Connexion utilisateur"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': 'Username et password requis'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        profile = UserProfile.objects.get(user=user)
        
        return Response({
            'success': True,
            'message': 'Connexion réussie',
            'user_id': user.id,
            'username': user.username,
            'token': token.key,
            'profile': {
                'specialite': profile.specialite,
                'niveau_expertise': profile.niveau_expertise,
                'domaine': profile.domaine
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Identifiants invalides'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Récupération du profil utilisateur"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        
        return Response({
            'success': True,
            'profile': serializer.data
        }, status=status.HTTP_200_OK)
    
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Profil non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Mise à jour du profil utilisateur"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        # Mise à jour des champs autorisés
        if 'specialite' in request.data:
            profile.specialite = request.data['specialite']
        if 'niveau_expertise' in request.data:
            profile.niveau_expertise = request.data['niveau_expertise']
        if 'domaine' in request.data:
            profile.domaine = request.data['domaine']
        
        profile.save()
        
        serializer = UserProfileSerializer(profile)
        return Response({
            'success': True,
            'message': 'Profil mis à jour',
            'profile': serializer.data
        }, status=status.HTTP_200_OK)
    
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Profil non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Déconnexion utilisateur"""
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        
        return Response({
            'success': True,
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)
    
    except Token.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Token non trouvé'
        }, status=status.HTTP_400_BAD_REQUEST)
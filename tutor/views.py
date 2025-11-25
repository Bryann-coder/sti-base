from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import TutorService
import json

class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            data = request.data
            message = data.get('message', '')
            session_id = data.get('session_id')
            
            if not message:
                return Response({'error': 'Message requis'}, status=status.HTTP_400_BAD_REQUEST)
            
            tutor_service = TutorService(request.user)
            resultat = tutor_service.handle_interaction(message, session_id)
            
            return Response({'success': True, 'data': resultat}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProgressionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            tutor_service = TutorService(request.user)
            progression = tutor_service.get_progression()
            return Response({'success': True, 'data': progression}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SessionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            return Response({'success': True, 'message': 'Prêt pour une nouvelle session'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, session_id):
        try:
            tutor_service = TutorService(request.user)
            success = tutor_service.terminer_session(session_id)
            
            if success:
                return Response({'success': True, 'message': 'Session terminée'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Session non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

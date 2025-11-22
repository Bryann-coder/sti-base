from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .services import TutorService
import json

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ChatView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            session_id = data.get('session_id')
            
            if not message:
                return JsonResponse({'error': 'Message requis'}, status=400)
            
            tutor_service = TutorService(request.user)
            resultat = tutor_service.handle_interaction(message, session_id)
            
            return JsonResponse({'success': True, 'data': resultat})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(login_required, name='dispatch')
class ProgressionView(View):
    def get(self, request):
        try:
            tutor_service = TutorService(request.user)
            progression = tutor_service.get_progression()
            return JsonResponse({'success': True, 'data': progression})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SessionView(View):
    def post(self, request):
        try:
            return JsonResponse({'success': True, 'message': 'Prêt pour une nouvelle session'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def delete(self, request, session_id):
        try:
            tutor_service = TutorService(request.user)
            success = tutor_service.terminer_session(session_id)
            
            if success:
                return JsonResponse({'success': True, 'message': 'Session terminée'})
            else:
                return JsonResponse({'error': 'Session non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import InteractionInputSerializer, InteractionOutputSerializer
from .models import LearnerProfile
from tutor.services import TutorService # On importe le cerveau !

class TutorInteractionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 1. Valider l'entrée de l'utilisateur
        input_serializer = InteractionInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Récupérer le profil de l'apprenant
        try:
            learner_profile = LearnerProfile.objects.get(user=request.user)
        except LearnerProfile.DoesNotExist:
            # Créer le profil s'il n'existe pas
            learner_profile = LearnerProfile.objects.create(user=request.user)

        # 3. Déléguer toute la logique au module Tutor
        user_message = input_serializer.validated_data['message']
        
        # Le service Tutor prend le contrôle
        tutor_service = TutorService(learner_profile)
        response_data = tutor_service.handle_interaction(user_message)

        # 4. Formater et renvoyer la réponse
        output_serializer = InteractionOutputSerializer(response_data)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
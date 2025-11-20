from rest_framework import serializers

class InteractionInputSerializer(serializers.Serializer):
    """
    Valide les données envoyées par l'utilisateur lors d'une interaction.
    """
    message = serializers.CharField(max_length=1000)
    # On pourrait ajouter un `session_id` pour suivre une conversation
    # session_id = serializers.UUIDField(required=False)

class InteractionOutputSerializer(serializers.Serializer):
    """
    Structure la réponse renvoyée par le tuteur.
    """
    tutor_response = serializers.CharField()
    current_concept_name = serializers.CharField()
    mastery_score = serializers.FloatField()
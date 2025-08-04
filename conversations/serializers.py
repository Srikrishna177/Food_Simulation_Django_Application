from rest_framework import serializers
from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    """Serialize Conversation model to JSON."""

    class Meta:
        model = Conversation
        fields = ['id', 'foods', 'vegetarian', 'vegan', 'created_at']
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Conversation
from django.db.models import Q
from .serializers import ConversationSerializer


class VegetarianVeganListView(generics.ListAPIView):
    """
    Returns a list of conversations where the user is vegetarian or vegan.
    Uses basic HTTP authentication; only authenticated users can access.
    """

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter conversations where vegetarian or vegan is True
        return Conversation.objects.filter(Q(vegetarian=True) | Q(vegan=True)).order_by('-created_at')
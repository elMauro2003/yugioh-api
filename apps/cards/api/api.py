from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from apps.cards.models import Card
from .serializers import CardSerializer
from .pagination import CardPagination
from .filters import CardFilter

class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    pagination_class = CardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CardFilter

class CardDetailView(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardCreateView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

class CardUpdateView(generics.UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

class CardDeleteView(generics.DestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]
from rest_framework import generics
from apps.cards.models import Card
from .serializers import CardSerializer
from .pagination import CardPagination

class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    pagination_class = CardPagination

class CardDetailView(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardCreateView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardUpdateView(generics.UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardDeleteView(generics.DestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
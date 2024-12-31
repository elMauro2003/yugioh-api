from rest_framework import viewsets
from apps.cards.models import Card
from .serializers import CardSerializer
from .pagination import CardPagination


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    pagination_class = CardPagination
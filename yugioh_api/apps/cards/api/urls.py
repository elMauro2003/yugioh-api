from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.cards.api.api import CardViewSet

router = DefaultRouter()
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
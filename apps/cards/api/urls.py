from django.urls import path
from .api import CardListView, CardDetailView, CardCreateView, CardDeleteView, CardUpdateView

urlpatterns = [
    path('cards/', CardListView.as_view(), name='card_list'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('cards/create/', CardCreateView.as_view(), name='card_create'),
    path('cards/delete/<int:pk>/', CardDeleteView.as_view(), name='card_delete'),
    path('cards/update/<int:pk>/', CardUpdateView.as_view(), name='card_update'),
]
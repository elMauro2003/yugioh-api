
from django.urls import path
from apps.users.api.api import RegisterUserView, AssignAPIKeyView, Login, Logout

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('assign-api-key/', AssignAPIKeyView.as_view(), name='assign_api_key'),
]

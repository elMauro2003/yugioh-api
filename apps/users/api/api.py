from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_api_key.models import APIKey
from apps.users.api.serializers import UserSerializer
from apps.users.models import ActiveSession
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class AssignAPIKeyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        api_key, key = APIKey.objects.create_key(name=username)
        return Response({"api_key": key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar si el usuario ya tiene una sesión activa
            active_sessions = ActiveSession.objects.filter(user=user)
            if active_sessions.exists():
                # Cerrar todas las sesiones activas existentes
                for session in active_sessions:
                    session.delete()
                logout(request)
            
            # Crear una nueva sesión
            session_token = get_random_string(length=32)
            ActiveSession.objects.create(user=user, session_token=session_token)
            login(request, user)
            return Response({"message": "Login successful", "session_token": session_token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            active_session = ActiveSession.objects.get(user=user)
            # Mostrar por consola el nombre del usuario que accedió
            # print(f"User {user.username} is logging out.")
            active_session.delete()
            logout(request)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except ActiveSession.DoesNotExist:
            return Response({"detail": "Active session not found."}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_api_key.models import APIKey
from django.contrib.auth import get_user_model

from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework import status
from apps.users.api.serializers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from apps.users.api.serializers import UserTokenSerializer
from apps.users.models import ActiveSession
from django.utils.crypto import get_random_string

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



"""
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
"""


class Login(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request': request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serialized = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serialized.data,
                        'message': 'Login successful'
                    }, status=status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'user': user_serialized.data,
                        'message': 'Login successful'
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error' : 'Este usuario no puede iniciar sesión'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error' : 'Nombre de usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response('Just an empty response', status=status.HTTP_204_NO_CONTENT)


from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from datetime import datetime

class Logout(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            token_key = request.GET.get('token')
            token = Token.objects.filter(key=token_key).first()
            
            if token:
                user = token.user
                
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                session_message = 'Sesiones de usuario cerradas'
                token_message = 'Token eliminado'
                return Response({'token_message': token_message, 'session_message': session_message}, status=status.HTTP_200_OK)

            return Response({'error': 'No se ha encontrado un usuario con estas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'No se ha encontrado token en la petición', 'details': str(e)}, status=status.HTTP_409_CONFLICT)
            
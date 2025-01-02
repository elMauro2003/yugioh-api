from celery import shared_task
from rest_framework_api_key.models import APIKey
from django.contrib.auth import get_user_model
from apps.users.models import User

#User = get_user_model()

@shared_task
def update_api_keys():
    users = User.objects.all()
    for user in users:
        # Eliminar la API Key existente
        APIKey.objects.filter(name=user.username).delete()
        # Crear una nueva API Key
        api_key, key = APIKey.objects.create_key(name=user.username)
        # Aquí puedes enviar la nueva API Key al usuario por correo electrónico o guardarla en algún lugar seguro
        print(f"Updated API Key for {user.username}: {key}")
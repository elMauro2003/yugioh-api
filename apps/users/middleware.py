from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from rest_framework_api_key.models import APIKey

class CheckAPIKeyExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith("Api-key "):
            # Extraer la clave completa después del espacio
            api_key_full = authorization_header.split(" ")[1]
            # Mensaje de depuración
            print(f"Extracted API Key: {api_key_full}")  
            
            try:
                api_key_obj = APIKey.objects.get_from_key(api_key_full)
                if api_key_obj and api_key_obj.has_expired:
                    # Eliminar la API Key existente
                    api_key_obj.delete()
                    # Crear una nueva API Key
                    new_api_key, key = APIKey.objects.create_key(name=api_key_obj.name)
                    # Establecer la fecha de vencimiento a 10 días a partir de ahora
                    new_api_key.expiry_date = now() + timedelta(days=10)
                    print(new_api_key.expiry_date)
                    new_api_key.save()
                    return JsonResponse({"message": "API Key expired. Here is your new API Key.", "new_api_key": key}, status=401)
            except APIKey.DoesNotExist:
                return JsonResponse({"error": "Invalid API Key"}, status=401)
        
        response = self.get_response(request)
        return response
import requests
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import Yu-Gi-Oh cards from YGOPRODeck API'

    def handle(self, *args, **kwargs):
        # URL de la API
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

        # Hacer la solicitud GET a la API
        response = requests.get(url)

        # Verificar que la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta a JSON
            data = response.json()
            
            # Solicitar al usuario la cantidad de cartas a guardar.
            cantidad = input("Ingrese la cantidad de cartas a guardar (o presione Enter para guardar todas): ")
            
            # Procesar cada carta para incluir el ID de Konami
            for card in data['data']:
                card['konami_id'] = card.pop('id', None)
            
            # Si el usuario ingresó una cantidad, convertirla a entero y seleccionar esa cantidad de cartas
            if cantidad.isdigit():
                cantidad = int(cantidad)
                data['data'] = data['data'][:cantidad]
            
            # Nombre del archivo a guardar
            fileName = 'data.json'
            
            # Guardar los datos JSON en un archivo local
            with open(fileName, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Datos guardados exitosamente (cantidad: {len(data['data'])})")
        else:
            print(f"Error al hacer la solicitud: {response.status_code}")
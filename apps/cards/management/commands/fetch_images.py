import json
import requests
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from django.core.management.base import BaseCommand
from tqdm import tqdm

def descargar_imagenes(json_file, start_index, end_index, tipo_imagen='all'):
    # Leer el archivo JSON
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Asegurarse de que data sea una lista
    if isinstance(data, dict):
        data = data.get('data', [])  # Ajusta 'data' según la estructura de tu JSON
    
    # Verificar y crear directorios si no existen
    directories = ['media/cards', 'media/cards_small', 'media/cards_cropped']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Inicializar la barra de progreso
    total_images = sum(len(objeto.get('card_images', [])) for objeto in data[start_index:end_index])
    progress_bar = tqdm(total=total_images, desc='Descargando imágenes', unit='imagen', dynamic_ncols=True)

    # Iterar sobre los objetos y descargar las imágenes
    for i, objeto in enumerate(data[start_index:end_index]):
        card_images = objeto.get('card_images', [])
        if card_images:
            for j, image_info in enumerate(card_images):
                urls = []
                if tipo_imagen == 'all':
                    urls = [
                        ('image_url', image_info.get('image_url')),
                        ('image_url_small', image_info.get('image_url_small')),
                        ('image_url_cropped', image_info.get('image_url_cropped'))
                    ]
                else:
                    urls = [(tipo_imagen, image_info.get(tipo_imagen))]

                for tipo, url in urls:
                    if url:
                        response = requests.get(url)
                        if response.status_code == 200:
                            if tipo == 'image_url':
                                directory = 'media/cards'
                            elif tipo == 'image_url_small':
                                directory = 'media/cards_small'
                            elif tipo == 'image_url_cropped':
                                directory = 'media/cards_cropped'
                            else:
                                continue

                            image_name = f"{directory}/{os.path.basename(url)}"
                            with open(image_name, 'wb') as img_file:
                                img_file.write(response.content)
                            progress_bar.update(1)
                        else:
                            print(f"Error al descargar la imagen: {url}")
    
    progress_bar.close()

class Command(BaseCommand):
    help = 'Descargar imágenes desde un archivo JSON'

    def handle(self, *args, **kwargs):
        # Ruta del archivo JSON
        file_path = os.path.join(os.path.dirname(__file__), '../../../../data.json')
        config_path = os.path.join(os.path.dirname(__file__), 'download_config.json')

        # Ocultar la ventana principal de Tkinter
        Tk().withdraw()

        # Leer configuración de descarga si existe
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
        else:
            config = {'last_index': 0}

        # Abrir un cuadro de diálogo para seleccionar el archivo JSON
        #json_file = askopenfilename(title="Seleccione el archivo JSON", filetypes=[("JSON files", "*.json")])
        
        json_file = os.path.join(os.path.dirname(__file__), '../../../../data.json')
        if json_file:
            cantidad = input("Ingrese la cantidad de objetos para descargar imágenes (o presione Enter para todos): ")
            cantidad = int(cantidad) if cantidad.isdigit() else None

            print("Seleccione el tipo de imagen a descargar:")
            print("1. image_url")
            print("2. image_url_small")
            print("3. image_url_cropped")
            print("4. Todas las anteriores")
            opcion = input("Ingrese el número de la opción deseada: ")

            tipo_imagen = 'all'
            if opcion == '1':
                tipo_imagen = 'image_url'
            elif opcion == '2':
                tipo_imagen = 'image_url_small'
            elif opcion == '3':
                tipo_imagen = 'image_url_cropped'

            # Leer el archivo JSON
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Determinar el índice de inicio
            start_index = config['last_index']
            end_index = start_index + cantidad if cantidad else len(data)

            # Descargar imágenes
            descargar_imagenes(json_file, start_index, end_index, tipo_imagen)

            # Actualizar configuración de descarga
            config['last_index'] = end_index
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file)
        else:
            print("No se seleccionó ningún archivo.")
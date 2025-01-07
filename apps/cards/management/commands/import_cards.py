import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.cards.models import Card, CardSet, CardImage, CardPrice
from django.db.utils import IntegrityError
from termcolor import colored
from colorama import init
from tqdm import tqdm


# Inicializar colorama
init()

class Command(BaseCommand):
    help = 'Import Yu-Gi-Oh cards from a JSON file'

    def handle(self, *args, **kwargs):
        # Especifica la ruta completa al archivo data.json
        file_path = os.path.join(os.path.dirname(__file__), '../../../../data.json')
        
        with open(file_path, 'r') as file:
            data = json.load(file)

        total_cards = len(data['data'])
        progress_bar = tqdm(total=total_cards, desc='Importando cartas', unit='carta', dynamic_ncols=True)

        for card_data in data['data']:
            card_sets_data = card_data.pop('card_sets', [])
            card_images_data = card_data.pop('card_images', [])
            card_prices_data = card_data.pop('card_prices', [])

            # Asegúrate de que 'level' y otros campos tengan valores predeterminados
            level = card_data.get('level', None)
            atk = card_data.get('atk', None)
            defense = card_data.get('def', None)
            linkval = card_data.get('linkval', None)
            linkmarkers = card_data.get('linkmarkers', [])
            pend_desc = card_data.get('pend_desc', None)
            monster_desc = card_data.get('monster_desc', None)
            scale = card_data.get('scale', None)

            # Verificar si la carta ya existe
            konami_id = card_data['konami_id']
            if Card.objects.filter(konami_id=konami_id).exists():
                message = colored(f'La carta "{card_data["name"]}" con konami_id {konami_id} ya existe.', 'yellow')
                progress_bar.write(message)
                progress_bar.update(1)
                continue

            # Crear la carta si no existe
            card, created = Card.objects.get_or_create(
                konami_id=konami_id,
                defaults={
                    'name': card_data['name'],
                    'typeline': card_data.get('typeline', []),
                    'type': card_data.get('type', ''),
                    'humanReadableCardType': card_data.get('humanReadableCardType', ''),
                    'frameType': card_data.get('frameType', ''),
                    'desc': card_data.get('desc', ''),
                    'race': card_data.get('race', ''),
                    'atk': atk,
                    'defense': defense,
                    'level': level,
                    'attribute': card_data.get('attribute', ''),
                    'archetype': card_data.get('archetype', None),
                    'linkval': linkval,
                    'linkmarkers': linkmarkers,
                    'ygoprodeck_url': card_data.get('ygoprodeck_url', ''),
                    'pend_desc': pend_desc,
                    'monster_desc': monster_desc,
                    'scale': scale
                }
            )

            message = colored(f'Carta "{card.name}" con konami_id {konami_id} agregada.', 'green')
            progress_bar.write(message)

            for card_set_data in card_sets_data:
                try:
                    card_set, created = CardSet.objects.get_or_create(
                        set_name=card_set_data['set_name'],
                        set_code=card_set_data['set_code'],
                        defaults={
                            'set_rarity': card_set_data['set_rarity'],
                            'set_rarity_code': card_set_data['set_rarity_code'],
                            'set_price': card_set_data['set_price']
                        }
                    )
                except CardSet.MultipleObjectsReturned:
                    card_set = CardSet.objects.filter(
                        set_name=card_set_data['set_name'],
                        set_code=card_set_data['set_code']
                    ).first()
                card.card_sets.add(card_set)

            for card_image_data in card_images_data:
                # Suponiendo que 'konami_id' es un atributo del objeto 'card'
                konami_id = card.konami_id

                # Construir las rutas de los archivos de imagen
                image_url = f'https://{settings.DOMAIN_URL}/media/cards/{konami_id}.jpg'
                image_url_small = f'https://{settings.DOMAIN_URL}/media/cards_small/{konami_id}.jpg'
                image_url_cropped = f'https://{settings.DOMAIN_URL}/media/cards_cropped/{konami_id}.jpg'

                # Verificar si los archivos existen
                if not os.path.exists(f'./media/cards/{konami_id}.jpg'):
                    image_url = 'None'
                if not os.path.exists(f'./media/cards_small/{konami_id}.jpg'):
                    image_url_small = 'None'
                if not os.path.exists(f'./media/cards_cropped/{konami_id}.jpg'):
                    image_url_cropped = 'None'

                # Crear el objeto CardImage con las URLs verificadas
                CardImage.objects.create(
                    card=card,
                    image_url=image_url,
                    image_url_small=image_url_small,
                    image_url_cropped=image_url_cropped
                )

            for card_price_data in card_prices_data:
                CardPrice.objects.create(
                    card=card,
                    cardmarket_price=card_price_data['cardmarket_price'],
                    tcgplayer_price=card_price_data['tcgplayer_price'],
                    ebay_price=card_price_data['ebay_price'],
                    amazon_price=card_price_data['amazon_price'],
                    coolstuffinc_price=card_price_data['coolstuffinc_price']
                )

            progress_bar.update(1)

        progress_bar.close()

        # Mensaje de éxito parpadeante
        success_message = colored('Successfully imported cards', 'green', attrs=['blink'])
        self.stdout.write(success_message)
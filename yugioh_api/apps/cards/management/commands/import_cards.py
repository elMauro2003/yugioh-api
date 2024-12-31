import json
import os
from django.core.management.base import BaseCommand
from apps.cards.models import Card, CardSet, CardImage, CardPrice
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Import Yu-Gi-Oh cards from a JSON file'

    def handle(self, *args, **kwargs):
        # Especifica la ruta completa al archivo data.json
        file_path = os.path.join(os.path.dirname(__file__), '../../../../data.json')
        
        with open(file_path, 'r') as file:
            data = json.load(file)

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

            card, created = Card.objects.get_or_create(
                name=card_data['name'],
                defaults={
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
                    'ygoprodeck_url': card_data.get('ygoprodeck_url', '')
                }
            )

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
                CardImage.objects.create(
                    card=card,
                    image_url=card_image_data['image_url'],
                    image_url_small=card_image_data['image_url_small'],
                    image_url_cropped=card_image_data['image_url_cropped']
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

        self.stdout.write(self.style.SUCCESS('Successfully imported cards'))
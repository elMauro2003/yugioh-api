from rest_framework import serializers
from apps.cards.models import Card, CardSet, CardImage, CardPrice

class CardSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardSet
        fields = '__all__'

class CardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardImage
        fields = '__all__'
        extra_kwargs = {'card': {'required': False}}

class CardPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardPrice
        fields = '__all__'
        extra_kwargs = {'card': {'required': False}}

class CardSerializer(serializers.ModelSerializer):
    card_sets = CardSetSerializer(many=True, required=False)
    card_images = CardImageSerializer(many=True, required=False)
    card_prices = CardPriceSerializer(many=True, required=False)

    class Meta:
        model = Card
        fields = '__all__'

    def create(self, validated_data):
        card_sets_data = validated_data.pop('card_sets', [])
        card_images_data = validated_data.pop('card_images', [])
        card_prices_data = validated_data.pop('card_prices', [])
        
        # Manejar el campo id opcionalmente
        card_id = validated_data.pop('id', None)
        if card_id and not Card.objects.filter(id=card_id).exists():
            card = Card(id=card_id, **validated_data)
            card.save(force_insert=True)
        else:
            card = Card.objects.create(**validated_data)
        
        # Crear instancias de CardSet y agregarlas a la relación ManyToMany
        card_sets = []
        for card_set_data in card_sets_data:
            card_set_qs = CardSet.objects.filter(
                set_name=card_set_data['set_name'],
                set_code=card_set_data['set_code']
            )
            if card_set_qs.exists():
                card_set = card_set_qs.first()
            else:
                card_set = CardSet.objects.create(**card_set_data)
            card_sets.append(card_set)
        card.card_sets.set(card_sets)
        
        # Crear instancias de CardImage
        for card_image_data in card_images_data:
            CardImage.objects.create(card=card, **card_image_data)
        
        # Crear instancias de CardPrice
        for card_price_data in card_prices_data:
            CardPrice.objects.create(card=card, **card_price_data)
        
        return card
    
    def update(self, instance, validated_data):
        card_sets_data = validated_data.pop('card_sets')
        card_images_data = validated_data.pop('card_images')
        card_prices_data = validated_data.pop('card_prices')

        instance.name = validated_data.get('name', instance.name)
        instance.typeline = validated_data.get('typeline', instance.typeline)
        instance.type = validated_data.get('type', instance.type)
        instance.human_readable_card_type = validated_data.get('human_readable_card_type', instance.human_readable_card_type)
        instance.frame_type = validated_data.get('frame_type', instance.frame_type)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.race = validated_data.get('race', instance.race)
        instance.atk = validated_data.get('atk', instance.atk)
        instance.defense = validated_data.get('defense', instance.defense)
        instance.level = validated_data.get('level', instance.level)
        instance.attribute = validated_data.get('attribute', instance.attribute)
        instance.archetype = validated_data.get('archetype', instance.archetype)
        instance.linkval = validated_data.get('linkval', instance.linkval)
        instance.linkmarkers = validated_data.get('linkmarkers', instance.linkmarkers)
        instance.ygoprodeck_url = validated_data.get('ygoprodeck_url', instance.ygoprodeck_url)
        instance.save()

        instance.card_sets.clear()
        for card_set_data in card_sets_data:
            card_set, created = CardSet.objects.get_or_create(**card_set_data)
            instance.card_sets.add(card_set)

        instance.card_images.all().delete()
        for card_image_data in card_images_data:
            CardImage.objects.create(card=instance, **card_image_data)

        instance.card_prices.all().delete()
        for card_price_data in card_prices_data:
            CardPrice.objects.create(card=instance, **card_price_data)

        return instance
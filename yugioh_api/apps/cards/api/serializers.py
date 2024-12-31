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

class CardPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardPrice
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    card_sets = CardSetSerializer(many=True, read_only=True)
    card_images = CardImageSerializer(many=True, read_only=True)
    card_prices = CardPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = '__all__'

    def create(self, validated_data):
        card_sets_data = validated_data.pop('card_sets')
        card_images_data = validated_data.pop('card_images')
        card_prices_data = validated_data.pop('card_prices')
        card = Card.objects.create(**validated_data)
        for card_set_data in card_sets_data:
            CardSet.objects.create(card=card, **card_set_data)
        for card_image_data in card_images_data:
            CardImage.objects.create(card=card, **card_image_data)
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
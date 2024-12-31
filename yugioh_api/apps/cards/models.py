from django.db import models

class CardSet(models.Model):
    set_name = models.CharField(max_length=255)
    set_code = models.CharField(max_length=255)
    set_rarity = models.CharField(max_length=255)
    set_rarity_code = models.CharField(max_length=255)
    set_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.set_name

class CardImage(models.Model):
    card = models.ForeignKey('Card', related_name='card_images', on_delete=models.CASCADE)
    image_url = models.URLField()
    image_url_small = models.URLField()
    image_url_cropped = models.URLField()

class CardPrice(models.Model):
    card = models.ForeignKey('Card', related_name='card_prices', on_delete=models.CASCADE)
    cardmarket_price = models.DecimalField(max_digits=10, decimal_places=2)
    tcgplayer_price = models.DecimalField(max_digits=10, decimal_places=2)
    ebay_price = models.DecimalField(max_digits=10, decimal_places=2)
    amazon_price = models.DecimalField(max_digits=10, decimal_places=2)
    coolstuffinc_price = models.DecimalField(max_digits=10, decimal_places=2)

class Card(models.Model):
    name = models.CharField(max_length=255)
    typeline = models.JSONField()
    type = models.CharField(max_length=255)
    human_readable_card_type = models.CharField(max_length=255)
    frame_type = models.CharField(max_length=255)
    desc = models.TextField()
    race = models.CharField(max_length=255)
    atk = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    attribute = models.CharField(max_length=255)
    archetype = models.CharField(max_length=255, null=True, blank=True)
    linkval = models.IntegerField(null=True, blank=True)
    linkmarkers = models.JSONField(null=True, blank=True)
    ygoprodeck_url = models.URLField()
    card_sets = models.ManyToManyField(CardSet, related_name='cards')

    def __str__(self):
        return self.name
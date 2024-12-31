from django.contrib import admin
from apps.cards.models import Card, CardSet, CardImage, CardPrice

class CardSetInline(admin.TabularInline):
    model = Card.card_sets.through
    extra = 1

class CardImageInline(admin.TabularInline):
    model = CardImage
    extra = 1

class CardPriceInline(admin.TabularInline):
    model = CardPrice
    extra = 1

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    inlines = [CardSetInline, CardImageInline, CardPriceInline]
    list_display = ('name', 'type', 'attribute', 'level')
    search_fields = ('name', 'type', 'attribute')

@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ('set_name', 'set_code', 'set_rarity', 'set_price')
    search_fields = ('set_name', 'set_code')

@admin.register(CardImage)
class CardImageAdmin(admin.ModelAdmin):
    list_display = ('card', 'image_url')
    search_fields = ('card__name',)

@admin.register(CardPrice)
class CardPriceAdmin(admin.ModelAdmin):
    list_display = ('card', 'cardmarket_price', 'tcgplayer_price', 'ebay_price', 'amazon_price', 'coolstuffinc_price')
    search_fields = ('card__name',)
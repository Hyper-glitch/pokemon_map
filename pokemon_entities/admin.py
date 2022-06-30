from django.contrib import admin

from .models import Pokemon, PokemonGeo


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    pass


@admin.register(PokemonGeo)
class PokemonGeoAdmin(admin.ModelAdmin):
    pass

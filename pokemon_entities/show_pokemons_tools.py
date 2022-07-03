import folium
from django.db.models import Q
from django.utils.timezone import localtime

from pokemon_entities.models import PokemonEntity


def add_pokemon_to_map(map, entity, url):
    icon = folium.features.CustomIcon(url, icon_size=(50, 50))
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], icon=icon).add_to(map)


def show_pokemons_on_map(request, folium_map):
    now = localtime()
    actual_pokemon_entities = PokemonEntity.objects.filter(Q(appeared_at__lt=now) & Q(disappeared_at__gt=now))

    for entity in actual_pokemon_entities:
        image_url = request.build_absolute_uri(entity.pokemon.image.url)
        add_pokemon_to_map(map=folium_map, entity=entity, url=image_url)

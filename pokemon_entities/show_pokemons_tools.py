"""Module that helps add and show pokemons to a map."""
import folium
from django.db.models import Q
from django.utils.timezone import localtime

from pokemon_entities.models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]


def show_pokemon_on_map(request, entity: PokemonEntity, folium_map):
    """Add pokemon entity to a map.
    :param request: request from template side.
    :param entity: pokemon's entity obj from database.
    :param folium_map: a map from folium libray  render pokemons.
    :return: None
    """
    image_url = request.build_absolute_uri(entity.pokemon.image.url)
    icon = folium.features.CustomIcon(image_url, icon_size=(50, 50))
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], icon=icon).add_to(folium_map)


def get_actual_pokemons(pokemon_id=None, show_all=True):
    now = localtime()
    all_entities = PokemonEntity.objects.filter(Q(appeared_at__lt=now) & Q(disappeared_at__gt=now))
    if not show_all:
        all_entities = all_entities.filter(pokemon__id=pokemon_id)
    return all_entities


def serialize_pokemon(request, pokemon, pokemon_id):
    previous_evolution = None
    serialized_next_evolution = None
    next_evolution_entity = PokemonEntity.objects.filter(pokemon__previous_evolution=pokemon_id).first()

    if next_evolution_entity:
        next_evolution = next_evolution_entity.pokemon
        serialized_next_evolution = {
            'title_ru': next_evolution.title_ru,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.image.url),
        }

    if pokemon.previous_evolution:
        previous_evolution = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
        }

    image_url = request.build_absolute_uri(pokemon.image.url)
    serialized_pokemon = {
        'img_url': image_url,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': serialized_next_evolution,
    }
    return serialized_pokemon

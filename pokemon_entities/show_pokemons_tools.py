"""Module that helps filter and show pokemons on a map."""
import folium
from django.db.models import Q
from django.utils.timezone import localtime

from pokemon_entities.models import PokemonEntity, Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]


def show_pokemon_on_map(request, entity: PokemonEntity, folium_map):
    """
    Add pokemon entity to a map.
    :param request: request from template side.
    :param entity: pokemon's entity obj from database.
    :param folium_map: a map from folium libray  render pokemons.
    :return: None
    """
    image_url = request.build_absolute_uri(entity.pokemon.image.url)
    icon = folium.features.CustomIcon(image_url, icon_size=(50, 50))
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], icon=icon).add_to(folium_map)


def get_actual_pokemons(pokemon_id=None, show_all=None):
    """
    Filter pokemon's entities from database in order to appeared and disappeared time. Also could show all pokemons.
    :param pokemon_id: id of a pokemon obj.
    :param show_all: flag that control to render all pokemons or one entity.
    :return: all_entities: filtered entities queryset.
    """
    now = localtime()
    all_entities = PokemonEntity.objects.filter(Q(appeared_at__lt=now) & Q(disappeared_at__gt=now))
    if not show_all:
        all_entities = all_entities.filter(pokemon__id=pokemon_id)
    return all_entities


def serialize_pokemon(request, pokemon: Pokemon) -> dict:
    """
    Serialize current pokemon with next and previous evolution.
    :param request: request from template side.
    :param pokemon: pokemon obj from database.
    :return: serialized_pokemon: serialized pokemon's information.
    """
    previous_evolution = None
    serialized_next_evolution = None
    next_evolution_entity = pokemon.next_evolutions.first()

    if next_evolution_entity:
        serialized_next_evolution = {
            'title_ru': next_evolution_entity.title_ru,
            'pokemon_id': next_evolution_entity.id,
            'img_url': request.build_absolute_uri(next_evolution_entity.image.url),
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

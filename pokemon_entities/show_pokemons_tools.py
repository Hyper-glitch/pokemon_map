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
    detailed_info = prepare_detailed_info(entity=entity)
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], popup=detailed_info, icon=icon).add_to(folium_map)


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
    elements = pokemon.elements.all()

    if next_evolution_entity:
        serialized_next_evolution = {
            'title_ru': next_evolution_entity.title_ru,
            'pokemon_id': next_evolution_entity.id,
            'img_url': build_uri(request, next_evolution_entity.image.url),
        }

    if pokemon.previous_evolution:
        previous_evolution = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': build_uri(request, pokemon.previous_evolution.image.url),
        }

    serialized_elements = [
        {
            'title': element.title,
            'img': build_uri(request, element.image.url),
            'strong_against': [element.title for element in element.strong_against.all()],
        }
        for element in elements
    ]

    serialized_pokemon = {
        'img_url': build_uri(request, pokemon.image.url),
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': serialized_next_evolution,
        'element_type': serialized_elements,
    }
    return serialized_pokemon


def prepare_detailed_info(entity: PokemonEntity) -> str:
    """
    Prepare data for detailed view of pokemon entity.
    :param entity: pokemon's entity obj from database.
    :return detailed_info: detailed pokemon's information.
    """
    description_slice = 7
    needful_fields = entity._meta.get_fields()[description_slice:]
    field_values = [entity.level, entity.health, entity.strength, entity.defence, entity.stamina]
    detailed_info = ''

    for field, value in zip(needful_fields, field_values):
        detailed_info += f'{field.verbose_name}: {value}\n'
    return detailed_info


def build_uri(request, url: str) -> str:
    """
    Build and return an absolute uri.
    :param request: request: request from template side.
    :param url: an url of image.
    :return: absolute uri.
    """
    return request.build_absolute_uri(url)

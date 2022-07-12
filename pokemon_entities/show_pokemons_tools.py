"""Module that helps filter and show pokemons on a map."""
import folium

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
            'img_url': request.build_absolute_uri(next_evolution_entity.image.url),
        }

    if pokemon.previous_evolution:
        previous_evolution = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
        }

    serialized_elements = [
        {
            'title': element.title,
            'img': request.build_absolute_uri(element.image.url),
            'strong_against': [element.title for element in element.strong_against.all()],
        }
        for element in elements
    ]

    serialized_pokemon = {
        'img_url': request.build_absolute_uri(pokemon.image.url),
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
    description_slice = 6
    serialize_pokemon_fields = PokemonEntity.pokemons.filter(pk=entity.pk).values()
    needed_fields = list(serialize_pokemon_fields[0].items())[description_slice:]
    detailed_info = ''

    for field in needed_fields:
        detailed_info += f'{field[0]}: {field[1]}\n'
    return detailed_info

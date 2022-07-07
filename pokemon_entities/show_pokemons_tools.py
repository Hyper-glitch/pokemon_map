"""Module that helps add and show pokemons to a map."""
import folium

from pokemon_entities.models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]


def show_pokemon_on_map(request, entity: PokemonEntity, folium_map):
    """Add pokemon entity to a map.
    :param request: request from template side.
    :param entity: pokemon's entity obj from database.
    :param folium_map: a map from folium libray.
    :return: None
    """
    image_url = request.build_absolute_uri(entity.pokemon.image.url)
    icon = folium.features.CustomIcon(image_url, icon_size=(50, 50))
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], icon=icon).add_to(folium_map)

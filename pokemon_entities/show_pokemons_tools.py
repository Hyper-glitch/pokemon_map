"""Module that helps add and show pokemons to a map."""
import folium

MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon_to_map(entity, url):
    """Add pokemon entity to a map.
    :param entity: pokemon's entity obj from database.
    :param url: absolute url for pokemon img.
    :return: None
    """
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    icon = folium.features.CustomIcon(url, icon_size=(50, 50))
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], icon=icon).add_to(folium_map)


def show_pokemons_on_map(request, entity):
    """

    :param request:
    :param entity:
    :return:
    """
    image_url = request.build_absolute_uri(entity.pokemon.image.url)
    add_pokemon_to_map(entity=entity, url=image_url)

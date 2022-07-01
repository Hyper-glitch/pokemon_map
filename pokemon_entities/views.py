import json

import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon_to_map(map, lat, lon, image_url):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon_entities:
        absolute_url = request.build_absolute_uri(entity.pokemon.image.url)
        add_pokemon_to_map(
            map=map, lat=entity.latitude, lon=entity.longitude,
            image_url=absolute_url,
        )

    serialized_pokemons = Pokemon.objects.all()
    pokemons_on_page = []

    for pokemon in serialized_pokemons:
        absolute_url = request.build_absolute_uri(pokemon.image.url)
        pokemons_on_page.append(
            {
                'pokemon_id': pokemon.id,
                'img_url': absolute_url,
                'title_ru': pokemon.title,
            }
        )
    context = {
        'map': map._repr_html_(),
        'pokemons': pokemons_on_page,
    }
    return render(request, 'mainpage.html', context=context)


def show_pokemon(request, pokemon_id):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    for pokemon in pokemons:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        add_pokemon_to_map(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon['img_url']
        )
    context = {'map': folium_map._repr_html_(), 'pokemon': pokemon}
    return render(request, 'pokemon.html', context=context)

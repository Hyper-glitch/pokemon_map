import json

import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon_to_map(map, entity, url):
    icon = folium.features.CustomIcon(url, icon_size=(50, 50))
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], icon=icon).add_to(map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    pokemons = []
    map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon_entities:
        image_url = request.build_absolute_uri(entity.pokemon.image.url)
        pokemons.append(
            {
                'pokemon_id': entity.pokemon.id,
                'img_url': image_url,
                'title_ru': entity.pokemon.title,
            }
        )
        add_pokemon_to_map(map=map, entity=entity, url=image_url)

    unique_pokemons = list({pokemon['pokemon_id']: pokemon for pokemon in pokemons}.values())
    context = {
        'map': map._repr_html_(),
        'pokemons': unique_pokemons,
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

import json

import folium
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from pokemon_entities.models import PokemonEntity, Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon_to_map(map, entity, url):
    icon = folium.features.CustomIcon(url, icon_size=(50, 50))
    # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
    folium.Marker([entity.latitude, entity.longitude], icon=icon).add_to(map)


def show_all_pokemons(request):
    now = localtime()
    actual_pokemon_entities = PokemonEntity.objects.filter(Q(appeared_at__lt=now) & Q(disappeared_at__gt=now))

    serialized_pokemons = []
    pokemons = Pokemon.objects.all()

    map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in actual_pokemon_entities:
        image_url = request.build_absolute_uri(entity.pokemon.image.url)
        add_pokemon_to_map(map=map, entity=entity, url=image_url)

    for pokemon in pokemons:
        image_url = request.build_absolute_uri(pokemon.image.url)
        serialized_pokemons.append(
            {
                'pokemon_id': pokemon.id,
                'img_url': image_url,
                'title_ru': pokemon.title,
            }
        )

    context = {
        'map': map._repr_html_(),
        'pokemons': serialized_pokemons,
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

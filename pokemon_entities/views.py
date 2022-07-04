import folium
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity
from pokemon_entities.show_pokemons_tools import show_pokemons_on_map

MOSCOW_CENTER = [55.751244, 37.618423]


def show_all_pokemons(request):
    serialized_pokemons = []
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.all()
    show_pokemons_on_map(request, folium_map)

    for pokemon in pokemons:
        image_url = request.build_absolute_uri(pokemon.image.url)
        serialized_pokemons.append(
            {
                'pokemon_id': pokemon.id,
                'img_url': image_url,
                'title_ru': pokemon.title_ru,
            }
        )

    context = {
        'map': folium_map._repr_html_(),
        'pokemons': serialized_pokemons,
    }

    return render(request, 'mainpage.html', context=context)


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    show_pokemons_on_map(request, folium_map)
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except (MultipleObjectsReturned, ObjectDoesNotExist):
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    image_url = request.build_absolute_uri(pokemon.image.url)
    previous_evolution = None
    serialized_next_evolution = None
    next_evolution_entity = PokemonEntity.objects.filter(pokemon__previous_evolution=pokemon_id).first()
    if next_evolution_entity:
        next_evolution = next_evolution_entity.pokemon
    else:
        next_evolution = None

    if pokemon.previous_evolution:
        previous_evolution = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
        }
    if next_evolution:
        serialized_next_evolution = {
            'title_ru': next_evolution.title_ru,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.image.url),
        }

    serialized_pokemon = {
        'img_url': image_url,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': serialized_next_evolution,
    }
    context = {'map': folium_map._repr_html_(), 'pokemon': serialized_pokemon}
    return render(request, 'pokemon.html', context=context)

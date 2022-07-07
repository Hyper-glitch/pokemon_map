import folium
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon
from pokemon_entities.show_pokemons_tools import show_pokemon_on_map, MOSCOW_CENTER, get_actual_pokemons, \
    serialize_pokemon


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    serialized_pokemons = []
    pokemons = Pokemon.objects.all()
    actual_pokemon_entities = get_actual_pokemons()

    for entity in actual_pokemon_entities:
        show_pokemon_on_map(request=request, entity=entity, folium_map=folium_map)

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
    actual_pokemon_entities = get_actual_pokemons(pokemon_id=pokemon_id, show_all=False)

    for entity in actual_pokemon_entities:
        show_pokemon_on_map(request=request, entity=entity, folium_map=folium_map)
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except (MultipleObjectsReturned, ObjectDoesNotExist):
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    serialized_pokemon = serialize_pokemon(request=request, pokemon=pokemon, pokemon_id=pokemon_id)
    context = {'map': folium_map._repr_html_(), 'pokemon': serialized_pokemon}

    return render(request, 'pokemon.html', context=context)

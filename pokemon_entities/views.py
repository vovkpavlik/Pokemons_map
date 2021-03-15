import folium

from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        img_url = request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon, img_url)

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            "pokemon_id": pokemon.id,
            "img_url": pokemon.photo.url,
            "title_ru": pokemon.title_ru,
        })
    return render(request, "mainpage.html", context={
        "map": folium_map._repr_html_(),
        "pokemons": pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entities = pokemon.pokemon_entities.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)


    pokemon_discription = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title_ru,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": pokemon.photo.url,
    }

    if pokemon.pre_evolution:
        pokemon_discription.update({
            "previous_evolution": {
                "title_ru": pokemon.pre_evolution.title_ru,
                "pokemon_id": pokemon.pre_evolution.id,
                "img_url": pokemon.pre_evolution.photo.url,
            }
        })

    if pokemon.next_evolution:
        pokemon_discription.update({
            "next_evolution": {
                "title_ru": pokemon.next_evolution.title_ru,
                "pokemon_id": pokemon.next_evolution.id,
                "img_url": pokemon.next_evolution.photo.url,
            }
        })

    for pokemon in pokemon_entities:
        img_url = request.build_absolute_uri(pokemon.pokemon.photo.url)
        add_pokemon(
            folium_map, pokemon.lat, pokemon.lon, img_url)

    return render(request, "pokemon.html", context={"map": folium_map._repr_html_(),
                                                    "pokemon": pokemon_discription,
                                                    })


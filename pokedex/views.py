from django.http.response import HttpResponse
from django.shortcuts import render
from pokedex.forms import PokemonForm

from pokedex.models import Pokemon


def index(request):
    return render(request, "pokedex/inicio.html")


def pokemon(request):

    if request.method == 'POST':
        pokemon = Pokemon(
            numero=request.POST['numero'], nombre=request.POST['nombre'], tipo=request.POST['tipo'])

        pokemon.save()

        return render(request, "pokedex/inicio.html")

    return render(request, "pokedex/pokemon.html")


def entrenador(request):
    return render(request, "pokedex/entrenador.html")


def pokeball(request):
    return render(request, "pokedex/pokeball.html")


def buscarPokemon(request):
    if request.GET['nombre']:
        nombre = request.GET['nombre']
        pokemons = Pokemon.objects.filter(nombre__icontains=nombre)

        return render(request, "pokedex/pokemon.html", {"pokemons": pokemons})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta)

from django.shortcuts import render

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


'''

API FORM

def pokemon(request):

    if request.method == 'POST':
        form = PokemonForm(request.POST)

        if form.is_valid():

            info = form.cleaned_data

            pokemon = Pokemon(
                nombre=info['nombre'], numero=info['numero'], tipo=info['tipo'])

            pokemon.save()

            return render(request, "pokedex/inicio.html")

    else:

        form = PokemonForm()

    return render(request, "pokedex/pokemon.html", {"form": form})'''


def entrenador(request):
    return render(request, "pokedex/entrenador.html")


def pokeball(request):
    return render(request, "pokedex/pokeball.html")

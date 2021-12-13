# TUTORIAL PASO A PASO

## Crear proyecto

`django-admin startproject project`

Esto crea la carpeta de nuestro proyecto

Dentro podemos tener varias apps

El enrutador principal de todas nuestras apps estara
en `urls.py` en la carpeta `project`

## Crear app

`python manage.py startapp pokedex`

Crea nuestra app en una carpeta separada

### Enrutador

Para acceder a la app debemos crear un enrutador y
vincularlo con el enrutador principal

Creamos el archivo `pokedex/urls.py`

Agregamos las vistas de nuestra app al router

```python
## pokedex/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('pokemon/', views.pokemon, name='pokemon'),
    path('pokeball/', views.pokeball, name='pokeball'),
    path('entrenador/', views.entrenador, name='entrenador'),
]
```

```python
## pokedex/views.py

from django.http import HttpResponse


def index(request):
    return HttpResponse("Vista principal.")


def pokemon(request):
    return HttpResponse("Vista Pokemon.")


def entrenador(request):
    return HttpResponse("Vista Entrenador.")


def pokeball(request):
    return HttpResponse("Vista Pokeball.")
```

Agregamos una ruta hacia nuestra app en el router principal:

```python
## project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('pokedex/', include('pokedex.urls')),
    path('admin/', admin.site.urls),
]
```

Hasta aqui tenemos la estructura principal de nuestro proyecto.

## Templates

Ahora necesitamos los templates para nuestras vistas

Dentro de la app creamos los siguientes archivos

```
pokedex
    /templates
        /pokedex
            inicio.html
            pokemon.html
            entrenador.html
            pokeball.html
```

Para poder leer los archivos necesitamos agregar nuestra app en la configuración del proyecto

```python
## project/settings.py

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pokedex' ## <--
]
```

Y ahora cambiamos las view para que devuelvan los archivos html

```
from django.shortcuts import render


def index(request):
    return render(request, "pokedex/inicio.html")


def pokemon(request):
    return render(request, "pokedex/pokemon.html")


def entrenador(request):
    return render(request, "pokedex/entrenador.html")


def pokeball(request):
    return render(request, "pokedex/pokeball.html")
```

## Diseño

Ahora que ya tenemos el esqueleto de nuestro proyecto y podemos acceder a cada una de las vistas.

Para diseñar nuestra app vamos a usar la libreria de estilos [Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/download/)

Descargamos los archivos.

Para poder importar estos archivos estaticos en nuestra web, debemos colocarlos en una nueva carpeta a la par de la carpeta templates

```
pokedex
    /templates
        ...
    /static
        /assets <- aqui pondremos imagenes e iconos
        /css <- aqui iran las hojas de estilo
        /js <- aqui iran scripts de javascript
        ...
```

Para poder cargar estos estilos necesitamos declararlo en nuestros templates

```html
<head>
  {% load static %}

  <link
    rel="stylesheet"
    type="text/css"
    href="{% static 'css/bootstrap.css' %}"
  />

  <meta charset="utf-8" />
  ....
</head>
```

Ya podemos ver reflejados los estilos en nuestra web

## Maquetado

Vamos a usar nuestro inicio como la vista principal,
que nos permita navegar entre formularios.

Nuestro inicio consistira de una barra de navegacion,
una vista cambiante y un footer con nuestros datos.

Para eso declaramos un bloque que recibira una vista de las que anteriormente
armamos

En nuestra vista principal `inicio.html` armamos la siguiente estructura

```html
<body>
  <!-- Navigation-->
  <nav class="navbar navbar-light bg-light static-top">...</nav>

  <!-- Sección que cambia -->
  <section>{% block formulario %} {% endblock %}</section>

  <!-- Footer-->
  <footer class="footer bg-light">...</footer>
</body>
```

El bloque formulario mostrara cualquiera de las vistas en la carpeta template
que contenga la etiqueta `extends` correspondiente a esta web.

Asi que vamos a completar cada una de las vistas con lo siguiente:

```html
{% extends "pokedex/inicio.html" %} {% load static %} {% block formulario %}

<h1>Pokeball</h1>

{% endblock %}
```

Tanto para entrenador, pokeball y pokemon. Ahora, como asociamos la vista
con el vinculo para navegar?

Debemos declarar los links de navegacion de la siguiente manera

```html
<nav class="navbar navbar-light bg-light static-top">
  <div class="container">
    <a class="navbar-brand" href="{% url 'inicio' %}">Pokedex</a>
    <ul class="nav">
      <li class="nav-item">
        <a class="nav-link active" aria-current="page" href="#">Inicio</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="{% url 'pokemon' %}">Pokemon</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="{% url 'entrenador' %}">Entrenador</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="{% url 'pokeball' %}">Pokeball</a>
      </li>
    </ul>
  </div>
</nav>
```

Listo, ahora podemos navegar entre nuestros formularios

## Modelos

En nuestro archivo `models.py` creamos los modelos por ejemplo el de pokemon

```python
from django.db import models


class Pokemon(models.Model):
    """
    Modelo que representa un Pokemon.
    """
    numero = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)

```

Y luego lo registramos en el `admin.py` para poder verlo en nuestro panel

```python
from django.contrib import admin
from .models import *

admin.site.register(Pokemon)
```

Cuando creemos un nuevo modelo debemos ejecutar

`python manage.py migrate`

para registrar correctamente en la base de datos los cambios

## Formularios

Existen dos metodos, via Modelo o via Formulario

### Modelo

Con un formulario comun

```
if request.method == 'POST':
        pokemon = Pokemon(
            numero=request.POST['numero'], nombre=request.POST['nombre'], tipo=request.POST['tipo'])

        pokemon.save()

        return render(request, "pokedex/inicio.html")
```

### Form API

Para este caso es necesario modificar el html pero nos permite agregar validacion en el controlador

Creamos un formulario en un archivo `forms.py`

```python
from django import forms


class PokemonForm(forms.Form):
    nombre = forms.CharField(max_length=30)
    numero = forms.IntegerField()
    tipo = forms.CharField(max_length=30)
```

Capturamos los datos en el endpoint y devolvemos un formulario

```python
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

    return render(request, "pokedex/pokemon.html", {"form": form})
```

En el HTML

```html
{% if form.errors %}

<p class="bg-warning">ERROR</p>

{% endif %}

<!-- API FORM -->
<form action="/pokedex/pokemon/" method="POST">
  {% csrf_token %}
  <table>
    {{form.as_table}}
  </table>
  <button class="btn btn-primary" type="submit" value="Enviar">Enviar</button>
</form>
```

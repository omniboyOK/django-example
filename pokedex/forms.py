from django import forms


class PokemonForm(forms.Form):
    nombre = forms.CharField(max_length=30)
    numero = forms.IntegerField()
    tipo = forms.CharField(max_length=30)

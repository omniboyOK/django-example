from django.db import models


class Pokemon(models.Model):
    """
    Modelo que representa un Pokemon.
    """
    nombre = models.CharField(max_length=30)
    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=30)

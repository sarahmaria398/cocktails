
from django.db import models


class Cocktail(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    instructions = models.TextField()
    glass = models.CharField(max_length=200)
    is_popular = models.BooleanField()
    is_alcoholic = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(
        'Ingredient', related_name='ingredient', blank=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField()


from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext as _


class Cocktail(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    instructions = models.TextField()

    class Popular(models.TextChoices):
        ANY = 'AN', _('Any')
        POPULAR = 'PO', _('Popular')
        NOT_POPULAR = 'NO', _('Not Popular')

    is_popular = models.CharField(
        max_length=2,
        choices=Popular.choices,
        default=Popular.ANY
    )

    class Alcoholic(models.TextChoices):
        ANY = 'AN', _('Any')
        ALCOHOLIC = 'AL', _('Alcoholic')
        NOT_ALCOHOLIC = 'NO', _('Not Alcoholic')

    is_alcoholic = models.CharField(
        max_length=2,
        choices=Alcoholic.choices,
        default=Alcoholic.ANY
    )

    class Glass(models.TextChoices):
        ANY = 'AN', _('Any')
        HIGH_BALL = 'HI', _('Highball Glass')
        COCKTAIL = 'CO', _('Cocktail Glass')
        OLD_FASHIONED = 'OL', _('Old-fashioned Glass')
        WHISKEY = 'WH', _('Whiskey Glass')
        CHAMPAGNE_FLUTE = 'CH', _('Champagne Flute')
        COLLINS = 'CL', _('Collins Glass')
        POUSSE_CAFE_GLASS = 'PO', _('Pousse Cafe Glass')
        HURRICANE = 'HU', _('Hurricane Glass')
        IRISH_COFFEE_CUP = 'IR', _('Irish coffee cup')
        PUNCH_BOWL = 'PU', _('Punch Bowl')
        PITCHER = 'PT', _('Pitcher')
        PINT = 'PI', _('Pint Glass')
        COUPETTE_GLASS = 'CP', _('Coupette Glass')
        PARFAIT = 'PA', _('Parfait Glass')
        MARTINI = 'MA', _('Martini Glass')
        BALLOON = 'BA', _('Balloon Glass')
        COUPE = 'CU', _('Coupe Glass')

    glass = models.CharField(
        max_length=2,
        choices=Glass.choices,
        default=Glass.ANY
    )

    class Category(models.TextChoices):
        ANY = 'AN', _('Any')
        ORDINARY_DRINK = 'OR', _('Ordindary Drink')
        COCKTAIL = 'CO', _('Cocktail')
        SHAKE = 'SH', _('Shake')
        OTHER = 'OT', _('Other')
        COCOA = 'CA', _('Cocoa')
        SHOT = 'ST', _('Shot')
        COFFEE_TEA = 'CE', _('Coffee Tea')
        HOMEMADE_LIQUEUR = 'HO', _('Homemade Liqueur')
        PUNCH = 'PU', _('Punch')
        BEER = 'BE', _('Beer')
        SOFT_DRINK = 'SO', _('Soft Drink')

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.ANY
    )

    ingredients = models.ManyToManyField(
        'Ingredient', related_name='ingredient', blank=True)

    date_created = models.DateTimeField(default=datetime.now, blank=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField()

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('cocktails/popular', views.PopularCocktailList.as_view()),
    # returns list of popular cocktails
    path('cocktails', views.CocktailList.as_view()),
    # returns list of all cocktails
    path('cocktails/<int:pk>', views.CocktailDetail.as_view()),
    # returns single cocktail by id
    path('ingredients', views.IngredientList.as_view()),
    # returns list of all ingredients
    path('ingredients/<int:pk>', views.IngredientDetail.as_view()),
    # returns single ingredient by id
    path('cocktails/ingredients/<str:id1>/<str:id2>',
         views.CocktailIngredients.as_view()),
    #  parameter #1 is the ingredient id and param #2 is the cocktail id, adds or removes an ingredient from a cocktail
    path('cocktails/random', views.CocktailRandom.as_view()),
    # returns a random cocktail
    path('cocktails/<str:name>', views.CocktailByName.as_view()),
    # returns cocktail by its name
    path('ingredients/<str:name>', views.IngredientByName.as_view()),
    # returns ingredient by its name
    # path('cocktails/<str:letter>', views.CocktailByLetter.as_view()),
    path('cocktails/search/<str:ingredient>',
         views.CocktailByIngredient.as_view())
    # returns cocktails which match to the searched ingredient

]

urlpatterns = format_suffix_patterns(urlpatterns)

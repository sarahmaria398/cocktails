from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('cocktails/', views.CocktailList.as_view()),
    path('cocktails/<int:pk>', views.CocktailDetail.as_view()),
    path('ingredients/', views.IngredientList.as_view()),
    path('ingredients/<int:pk>', views.IngredientDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

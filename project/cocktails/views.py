from rest_framework.views import APIView
from rest_framework.response import Response
import random


from .models import Cocktail, Ingredient
from .serializers import CocktailSerializer, CocktailDetailSerializer, IngredientDetailSerializer, IngredientSerializer
from django.http import Http404
from rest_framework import status




class IngredientDetail(APIView):

    def get_object(self, pk):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            self.check_object_permissions(self.request, ingredient)
            return ingredient
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ingredient = self.get_object(pk)
        serializer = IngredientDetailSerializer(ingredient)
        return Response(serializer.data)

    def put(self, request, pk):
        ingredient = self.get_object(pk)
        data = request.data
        serializer = IngredientDetailSerializer(
            instance=ingredient,
            data=data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class IngredientList(APIView):

    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED
                            )
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST
                        )


class CocktailList(APIView):

    def get(self, request):
        cocktails = Cocktail.objects.all()
        serializer = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CocktailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED
                            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CocktailDetail(APIView):

    def get_object(self, pk):
        try:
            return Cocktail.objects.get(pk=pk)
        except Cocktail.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cocktail = self.get_object(pk)
        serializer = CocktailSerializer(cocktail)
        return Response(serializer.data)

    def put(self, request, pk):
        cocktail = self.get_object(pk)
        data = request.data
        serializer = CocktailDetailSerializer(
            instance=cocktail,
            data=data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CocktailIngredients(APIView):

    def get_object(self, id1):
        try:
            ingredient = Ingredient.objects.get(pk=id1)
            return ingredient
        except Ingredient.DoesNotExist:
            raise Http404

    def get_object_cocktail(self, id2):
        try:
            cocktail = Cocktail.objects.get(pk=id2)
            return cocktail
        except Cocktail.DoesNotExist:
            raise Http404

    def post(self, request, id1, id2):
        ingredient = self.get_object(id1)
        cocktail = self.get_object_cocktail(id2)

        if ingredient not in cocktail.ingredients.all():
            cocktail.ingredients.add(ingredient)
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id1, id2):
        ingredient = self.get_object(id1)
        cocktail = self.get_object_cocktail(id2)

        if ingredient in cocktail.ingredients.all():
            cocktail.ingredients.remove(ingredient)
            return Response(status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )


class CocktailRandom(APIView):

    def get(self, request):
        id = random.randint(1, len(Cocktail.objects.all()))
        cocktail = Cocktail.objects.get(pk=id)
        serializer = CocktailSerializer(cocktail)
        return Response(serializer.data)

class CocktailName(APIView):

    def get_object(self, name):
        try:
            return Cocktail.objects.get(name=name)
        except Cocktail.DoesNotExist:
            raise Http404
    
    def get(self, request, name):
        cocktail = self.get_object(name)
        serializer = CocktailSerializer(cocktail)
        return Response(serializer.data)
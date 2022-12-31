from rest_framework.views import APIView
from rest_framework.response import Response
import random


from .models import Cocktail, Ingredient
from .serializers import CocktailSerializer, CocktailDetailSerializer, IngredientDetailSerializer, IngredientSerializer
from django.http import Http404
from rest_framework import status
from django.db.models import Q


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

    # get single ingredient by pk

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
    # update the ingredient object by pk


class IngredientList(APIView):

    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
    # return list of all ingredients

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED
                            )
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST
                        )
    # post a new ingredient to the list of ingredients


class CocktailList(APIView):

    def get(self, request, *args, **kwargs):
        categories = request.query_params

        qs = Cocktail.objects.all()
        # return all cocktails

        is_popular = categories.get('is_popular')
        if categories.get('is_popular'):
            qs = qs.filter(is_popular=is_popular)
        is_alcoholic = categories.get('is_alcoholic')
        if categories.get('is_alcoholic'):
            qs = qs.filter(is_alcoholic=is_alcoholic)
        glass = categories.get('glass')
        if glass:
            qs = qs.filter(glass=glass)
        category = categories.get('category')
        if category:
            qs = qs.filter(category=category)
        # return filtered cocktails

        serializer = CocktailSerializer(qs, many=True)
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

        # post a new cocktail


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

        # get a single cocktail by pk

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

        # update a single cocktail by pk

    def delete(self, request, pk):
        cocktail = self.get_object(pk)
        cocktail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # delete a cocktail by pk


class CocktailIngredients(APIView):
    # post an ingredient object to a cocktail object, and also be able to remove it from the cocktail object

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

        # if the ingredient is not already in the ingredients field in the cocktail object, add it

    def delete(self, request, id1, id2):
        ingredient = self.get_object(id1)
        cocktail = self.get_object_cocktail(id2)

        if ingredient in cocktail.ingredients.all():
            cocktail.ingredients.remove(ingredient)
            return Response(status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )
    # if the ingredient is in the ingredients field in the cocktail object, remove it


class CocktailRandom(APIView):
    # return a random cocktail

    def get(self, request):

        id = random.randint(1, len(Cocktail.objects.filter(name__isnull=False)))
        if Cocktail.objects.filter(pk=id).exists():
            cocktails = Cocktail.objects.get(pk=id)
            serializer = CocktailSerializer(cocktails)
            return Response(serializer.data)
        else:
            cocktails = Cocktail.objects.get(pk=1)
            serializer = CocktailSerializer(cocktails)
            return Response(serializer.data)
        
        #a poor fix to the issue of returning non existant database items as the object has been deleted. 
        #currently, if object pk does not exist, if will return the first object in database, with pk 1
        #the queryset also is only based on the number of objects in the database, therefore not including objects with a higher pk number


class CocktailByName(APIView):
    # return a cocktail by its name

    def get_object(self, name):
        try:
            return Cocktail.objects.get(name=name)
        except Cocktail.DoesNotExist:
            raise Http404

    def get(self, request, name):
        cocktail = self.get_object(name)
        serializer = CocktailSerializer(cocktail)
        return Response(serializer.data)


class IngredientByName(APIView):
    # return an ingredient by its name

    def get_object(self, name):
        try:
            return Ingredient.objects.get(name=name)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, name):
        ingredient = self.get_object(name)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)


class PopularCocktailList(APIView):
    # return a list of Popular cocktails

    def get(self, request):
        cocktails = Cocktail.objects.filter(is_popular__exact='PO')
        serializer = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data)


class CocktailByIngredient(APIView):
    # return a list of cocktails which have an ingredient in it which has been selected

    def get(self, request, ingredient):
        cocktails = Cocktail.objects.filter(
            ingredients__name__exact=ingredient)
        serializer = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data)


class CocktailByLetter(APIView):
    # return list of cocktails which start with the selected letter

    def get(self, request, letter):
        cocktails = Cocktail.objects.filter(
            name__startswith=letter)
        serializer = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data)


class LatestCocktails(APIView):
    # get the ten most recently published cocktails

    def get(self, request):
        cocktails = Cocktail.objects.order_by('-date_created')[:10]
        serializer = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data)

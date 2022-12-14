from rest_framework import serializers
from .models import Cocktail, Ingredient


class IngredientSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    image = serializers.URLField()

    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)


class IngredientDetailSerializer(IngredientSerializer):

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)


class CocktailSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    image = serializers.URLField()
    instructions = serializers.CharField(max_length=1000)
    glass = serializers.CharField(max_length=2, required=False)
    is_popular = serializers.CharField(max_length=2, required=False)
    is_alcoholic = serializers.CharField(max_length=2, required=False)
    category = serializers.CharField(max_length=2, required=False)
    date_created = serializers.DateTimeField(required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    def create(self, validated_data):
        return Cocktail.objects.create(**validated_data)


class CocktailDetailSerializer(CocktailSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.instructions = validated_data.get(
            'instructions', instance.instructions)
        instance.image = validated_data.get('image', instance.image)
        instance.glass = validated_data.get('glass', instance.glass)
        instance.is_popular = validated_data.get(
            'is_popular', instance.is_popular)
        instance.is_alcoholic = validated_data.get(
            'is_alcoholic', instance.is_alcoholic)
        instance.category = validated_data.get(
            'category', instance.category)
        instance.date_created = validated_data.get(
            'date_created', instance.date_created)
        instance.save()
        return instance

    def create(self, validated_data):
        return Cocktail.objects.create(**validated_data)

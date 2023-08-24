from django.contrib.auth.models import User, Group 
from .models import Recipe
from rest_framework import serializers

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients']

from .models import Recipe
from .serializers import RecipeSerializer
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from collections import defaultdict
import requests


# Create your views here.

def recipe_form(request):
    title = request.GET.get('title')
    if title:
        api_url = f"http://127.0.0.1:8000/recipe/shopping-list/?title={title}" 
        response = requests.get(api_url)
        #print("Response Status Code: ", response.status_code)
        #print("Response Text: ", response.text)
        recipe = response.json()
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return render(request, 'recipe_form.html', {'recipe': recipe})
    

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_shopping_list(self, title, quantity):
        shopping_list = defaultdict(int)

        def accumulate_ingredients(recipe_title, recipe_quantity):
            recipe = Recipe.objects.get(title=recipe_title)
            ingredients = recipe.ingredients

            for ingredient_title, ingredient_quantity in ingredients.items():
                if ingredient_title.startswith("[") and ingredient_title.endswith("]"):
                    nested_recipe_title = ingredient_title[1:-1]
                    nested_recipe_quantity = int(ingredient_quantity) * recipe_quantity
                    accumulate_ingredients(nested_recipe_title, nested_recipe_quantity)
                else:
                    shopping_list[ingredient_title] += int(ingredient_quantity) * recipe_quantity

        accumulate_ingredients(title, quantity)
        return shopping_list

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def shopping_list(self, request):
        title = request.query_params.get("title", None)
        if not title:
            return Response({"error": "Title parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(title=title)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        shopping_list = self.get_shopping_list(title, 1)  # Initial quantity is 1
        sorted_shopping_list = dict(sorted(shopping_list.items(), key=lambda item: item[1], reverse=True))
        return Response(sorted_shopping_list, status=status.HTTP_200_OK)
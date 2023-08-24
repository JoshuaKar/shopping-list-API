from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.RecipeView.as_view({'get': 'list'}), name="recipe-list"),
    path('recipe/shopping-list/', views.RecipeView.as_view({'get': 'shopping_list'}), name='shopping-list'),
    path('recipe-form/', views.recipe_form, name='recipe-form'),
]
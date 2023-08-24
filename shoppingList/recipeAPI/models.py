from django.db import models
from django import forms 

# Create your models here
class Recipe(models.Model):
    title = models.CharField(max_length=50)
    ingredients = models.JSONField()
    
    def __str__(self):
        return self.title
    
class RecipeForm(forms.Form):
    recipe = forms.ChoiceField(label='Select a Recipe', choices=())
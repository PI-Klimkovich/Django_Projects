from django.urls import path
from .views import create_ingredient, create_recipe

# /food/

urlpatterns = [
    path("create_recipe/", create_recipe, name="create-recipe"),
    path("create_ingredient/", create_ingredient, name="create-ingredient"),
]

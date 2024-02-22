from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest

from .forms import RecipeForm, IngredientForm
from .models import Recipe, Ingredient


def home(request: WSGIRequest):
    return render(request, 'home.html', {"recipes": Recipe.objects.all()})


@login_required
def create_recipe(request: WSGIRequest):
    form = RecipeForm()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe: Recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            form.save_m2m()
            return HttpResponseRedirect("/")

    return render(request, 'recipe-form.html', {'form': form})


@login_required
def create_ingredient(request: WSGIRequest):
    form = IngredientForm()

    if request.method == 'POST':
        form = IngredientForm(request.POST, request.FILES)
        if form.is_valid():
            ingredient: Ingredient = form.save(commit=False)
            ingredient.user = request.user
            ingredient.save()
            form.save_m2m()

            return HttpResponseRedirect("/")

    return render(request, "create-ingredient.html", {"form": form})

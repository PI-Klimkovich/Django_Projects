from django import forms

from main_app.models import Recipe, Ingredient
from ckeditor.fields import CKEditorWidget


class RecipeCreationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'preview_image', 'category', 'ingredients', 'time_minutes', 'description']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "ingredients": forms.SelectMultiple(attrs={"class": "form-control"}),
            "description": CKEditorWidget(),
            "category": forms.Select(attrs={"class": "form-control"}),
            "preview_image": forms.FileInput(attrs={"class": "form-control"}),
            "time_minutes": forms.NumberInput(attrs={"class": "form-control"}),
        }


class IngredientCreationForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and Ingredient.objects.filter(name=name).exists():
            raise forms.ValidationError('Такой ингредиент уже существует')
        return name

    class Meta:
        model = Ingredient
        fields = ['name', 'description', 'calories']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": CKEditorWidget,
            "calories": forms.NumberInput(attrs={"class": "form-control"}),
        }


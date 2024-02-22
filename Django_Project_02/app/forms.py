from django import forms
from ckeditor.fields import CKEditorWidget

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ["name", "preview_image", "time_minutes", "category", "ingredients", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "preview_image": forms.FileInput(attrs={"class": "form-control"}),
            "time_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "ingredients": forms.SelectMultiple(attrs={"class": "form-control"}),
            "description": CKEditorWidget()
        }


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ["name", "calories", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": CKEditorWidget,
            "calories": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and Ingredient.objects.filter(name=name).exists():
            raise forms.ValidationError('Такой ингредиент уже существует')
        return name

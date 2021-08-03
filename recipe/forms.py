from django import forms 
from .models import ShoppingList

class ShoppingListChoiceForm(forms.ModelForm):
    list_choices = ShoppingList.objects.filter
    shopping_list = forms.ModelChoiceField(queryset=ShoppingList.objects.all())

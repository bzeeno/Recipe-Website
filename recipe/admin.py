from django.contrib import admin
from .models import Recipe, ShoppingList, Ingredient

admin.site.register(Recipe)
admin.site.register(ShoppingList)
admin.site.register(Ingredient)

from django.db import models
from django.contrib.auth.models import User
from users.models import Profile


# Shopping lists 
class ShoppingList(models.Model):
    name = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

# Table for recipes
class Recipe(models.Model):
    name = models.CharField(max_length=50, null=True)
    url = models.URLField(max_length=200, null=True)
    image = models.ImageField(default='default.jpg', upload_to='recipe_pics')
    summary = models.TextField(null=True)
    instructions = models.TextField(null=True)
    recipe_id = models.IntegerField(null=True)
    # A recipe can be in many shopping lists and a shopping list can have many recipes 
    shopping_lists = models.ManyToManyField(ShoppingList)
    profile = models.ManyToManyField(Profile)

    def __str__(self):
        return str(self.name)

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    measure_unit = models.CharField(max_length=15)
    # An ingredient can be in many recipes and a recipe can have many ingredients
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    

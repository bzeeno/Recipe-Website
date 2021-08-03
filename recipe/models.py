from django.db import models
from django.contrib.auth.models import User
from users.models import Profile


# Shopping lists 
class ShoppingList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

# Table for recipes
class Recipe(models.Model):
    recipe_id = models.IntegerField(null=True)
    name = models.CharField(max_length=50, null=True)
    image = models.ImageField(default='default.jpg', upload_to='recipe_pics')
    summary = models.TextField(null=True)
    instructions = models.TextField(null=True)
    # A recipe can be in many shopping lists and a shopping list can have many recipes 
    shopping_lists = models.ManyToManyField(ShoppingList)
    profile = models.ManyToManyField(Profile)

    def __str__(self):
        return str(self.name)

class Ingredient(models.Model):
    ingredient_id = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    measure_unit = models.CharField(max_length=15)
    # An ingredient can only be in one recipe, but a recipe can have many ingredients
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    

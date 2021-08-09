from django.db import models
from django.contrib.auth.models import User
from users.models import Profile


# Shopping lists 
class ShoppingList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
                                                                    # Shopping list is a child of Profile
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # A shopping list can only have one Profile, but a Profile can have many shopping lists

    def __str__(self):
        return str(self.name)

# Table for recipes
class Recipe(models.Model):
    recipe_id = models.IntegerField(null=True)
    name = models.CharField(max_length=150, null=True)
    image = models.ImageField(default='default.jpg', upload_to='recipe_pics')   # No default image (Maybe another time)
    summary = models.TextField(null=True)
    instructions = models.TextField(null=True)
    shopping_lists = models.ManyToManyField(ShoppingList)  # Shopping lists can have many recipes and recipes can be in many shopping lists
                                                           # Profiles will share Recipe objects since we don't want to make new recipes if it's already in our database
    profile = models.ManyToManyField(Profile)              # Profiles can have many recipes and recipes can be in many profiles

    def __str__(self):
        return str(self.name)

class Ingredient(models.Model):
    ingredient_id = models.IntegerField(null=True)
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    measure_unit = models.CharField(max_length=50)
                                                                  # Ingredient is a child of Recipe
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)  # An ingredient can only be in one recipe, but a recipe can have many ingredients

    def __str__(self):
        return str(self.name)

    

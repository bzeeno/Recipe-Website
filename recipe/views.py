from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django import forms 
from .models import Recipe, ShoppingList, Ingredient
import json
import ast
import spoonacular as sp

# Initialize Spoonacular API
api = sp.API(settings.API_KEY)
response = api.get_random_recipes(number=8) # get random recipes
random_recipes = response.json()            # Put random recipes in json object

############################################# HOME VIEW #############################################
class Home(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        # if there is not a session variable 'recipes' already made: create session variable
        if not request.session.get('recipes'):
            request.session['recipes'] = random_recipes
        return render(request, self.template_name, request.session['recipes'])

    def post(self, request):
        # If post request is search
        if 'query' in request.POST:
            query = request.POST.get('query-txt')                                                                   # Get query text
            response = api.search_recipes_complex(query, number=8, addRecipeInformation=True, fillIngredients=True) # Send post request to Spoonacular API
            recipes = response.json()
            recipes = recipes['results']                                                                            # Remove extra 'results' key returned by spoonacular API
            context = { 'recipes': recipes }
            return render(request, self.template_name, context)
        # If post request is add recipe (button on card)
        elif 'add-recipe' in request.POST:
            recipe_data = get_recipe_data(self,request)                                                             # Get recipe data
            add_recipe(self, request, recipe_data)                                                                  # Add recipe to database
            return render(request, self.template_name, self.request.session['recipes'])

    def form_valid(self, form, request):
        if 'add-recipe' in request.POST:
            form.instance.profile = self.request.user
            return super().form_valid(form)
#####################################################################################################



######################################## DASHBOARD LIST VIEW ########################################
class DashboardListView(ListView, LoginRequiredMixin):
    template_name = 'dashboard.html'

    def get(self, request):
        self.template_name = 'dashboard.html'
        recipes = Recipe.objects.filter(profile=self.request.user.profile)                                  # Get recipes associated w/current profile
        shopping_lists = ShoppingList.objects.filter(profile=self.request.user.profile)                     # Get shopping lists associated w/profile
        recipes_in_list = []

        # Get recipes for each shopping list (to display on dashboard)
        # Each list in recipes_in_list is associated with a shopping list
        for s_list in shopping_lists:
            new_recipe_list = []
            new_recipes = Recipe.objects.filter(profile=self.request.user.profile, shopping_lists=s_list)   # Get recipes associated with current shopping list
            new_recipe_list.append(new_recipes)                                                             # Add recipes to a list
            recipes_in_list.append(new_recipe_list)                                                         # Add list to another list
        context = {'recipes': recipes,
                   'shopping_lists': shopping_lists,
                   'recipes_in_list': recipes_in_list
        }
        return render(request, self.template_name, context)


    def post(self, request, **kwargs):
        # If user clicks button to add specific recipe to list
        # Send them to shopping list view to select shopping list
        if 'add-recipe' in request.POST:
            self.template_name = 'shopping_lists.html'
            recipe_data = get_recipe_data(self, request)
            render_page = ShoppingListsView.get(self, request, recipe_data=recipe_data)
            return render_page
        # If user selected which shopping list to add recipe to
        # Send post request to shopping list view
        elif 'add-recipe-list' in request.POST:
            render_page = ShoppingListsView.post(self, request)
            return render_page
        # If user clicked create list button
        # redirect to create list view
        elif 'create-list' in request.POST:
            return redirect('/create-list/')            
#####################################################################################################




######################################## RECIPE DETAILS VIEW ########################################
class RecipeDetailsView(TemplateView):
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe_data'

    def get(self, request, **kwargs):
        recipe_id = self.kwargs['recipeid']
        response = api.get_recipe_information(recipe_id)                                                # request recipe info from Spoonacular API
        recipe_data = response.json()
        # Boolean to tell if recipe is in profile
        if not request.user.is_anonymous:                                                               # if user is not anonymous (i.e. is logged in)
            if Recipe.objects.filter(recipe_id=recipe_id, profile=self.request.user.profile):
                is_user_recipe = True
            else:
                is_user_recipe = False
        else:
            is_user_recipe = False

        context = {
                'recipe_data': recipe_data, #request.session['recipe_data'],
                'is_user_recipe': is_user_recipe
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        if 'add-recipe' in request.POST:
            recipe_id = request.POST.get('recipe-id')
            recipe_data = get_recipe_data(self, request)
            add_recipe(self, request, recipe_data)
            return redirect('/recipe-details/'+str(recipe_id))
        # If user clicked delete recipe
        elif 'delete-recipe' in request.POST:
            recipe_id = request.POST.get('recipe-id')
            delete_recipe = Recipe.objects.get(recipe_id=recipe_id)                                     # Get recipe to delete
            current_profile = self.request.user.profile
            # Delete relationship between current profile and recipe. Also, remove recipe from shopping lists 
            delete_recipe.profile.remove(current_profile)
            delete_recipe.shopping_lists.clear()
            return redirect('/dashboard/')
#####################################################################################################



########################################## RECIPE LIST VIEW #########################################
class RecipeListView(ListView):
    template_name = 'recipe_list.html'

    def get(self, request, **kwargs):
        recipe_data = Recipe.objects.filter(profile=self.request.user.profile)

        context = {
                'recipe_data': recipe_data,
                'list_id': -1
        }
        return render(request, self.template_name, context)

    # If user clicked "My recipes" Link and wants to add a recipe to a shopping list
    # Send them to list view to choose which one
    def post(self, request, **kwargs):
        if 'add-recipe-list' in request.POST:
            return render(request, self.template_name, context)
#####################################################################################################



###################################### SHOPPING LIST CREATE VIEW ######################################
class CreateListView(CreateView):
    model = ShoppingList
    template_name = 'create_list.html'
    fields = ['name']

    def post(self, request):
        if 'create-list' in request.POST:
            name = request.POST.get('name')
            new_list = ShoppingList(name=name, profile=self.request.user.profile)
            new_list.save()
            listid = new_list.id
            return redirect('/list-details/'+str(listid))
#######################################################################################################



###################################### SHOPPING LIST LIST VIEW ######################################
class ShoppingListsView(TemplateView, LoginRequiredMixin):
    template_name = 'shopping_lists.html'

    def get(self, request, **kwargs):
        recipe_data = kwargs['recipe_data']
        shopping_lists = ShoppingList.objects.filter(profile=self.request.user.profile)                     # get shopping lists for current profile
        recipes_in_list = []                                                                                # will hold lists of recipes. Each list is associated with a shopping list.
        # get recipes associated with user's shopping lists
        for s_list in shopping_lists:
            new_recipe_list = []
            new_recipes = Recipe.objects.filter(profile=self.request.user.profile, shopping_lists=s_list)   # Get recipes associated w/current shopping list
            new_recipe_list.append(new_recipes)                                                             # Add recipes to list
            recipes_in_list.append(new_recipe_list)                                                         # Add list to other list
        context = {'shopping_lists': shopping_lists,
                   'recipes_in_list': recipes_in_list,
                   'recipe_data': recipe_data
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'add-recipe-list' in request.POST:
            recipe_data = get_recipe_data(self, request)
            list_id = request.POST.get('list-id')
            add_recipe_to_list(self, request, recipe_data, list_id)                                        
            render_page = DashboardListView.get(self, request)
            return render_page
######################################################################################################



###################################### SHOPPING LIST DETAIL VIEW #####################################
class ShoppingListDetailsView(DetailView, LoginRequiredMixin):
    model = ShoppingList
    template_name = 'list_detail.html'

    def get(self, request, **kwargs):
        list_id = self.kwargs['listid']
        list_data = ShoppingList.objects.filter(id=list_id, profile=self.request.user.profile)              # get specific list
        recipe_data = Recipe.objects.filter(profile=self.request.user.profile, shopping_lists__id=list_id)  # get recipes associated w/list
        ingredient_data = get_ingredients_in_recipe(self, request, recipe_data, list_id)                    # get ingredients associated w/recipes
         
        context = {'list_data': list_data,
                   'recipe_data': recipe_data,
                   'ingredient_data': ingredient_data
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        # If user clicked button to go to recipe page
        if 'add-to-list' in request.POST:
            list_id = request.POST.get('list-id')
            recipe_data = Recipe.objects.filter(profile=self.request.user.profile)
            context = {'recipe_data': recipe_data, 'list_id': list_id}
            return render(request, 'recipe_list.html', context)
        # If user clicked a recipe to add to list
        elif 'add-recipe-list' in request.POST:
            recipe_data = get_recipe_data(self, request)
            list_id = request.POST.get('list-id')
            add_recipe_to_list(self, request, recipe_data, list_id)
            render_page = self.get(request, listid=list_id)
            return render_page
        # If user clicked button to remove recipe from list
        elif 'remove-from-list' in request.POST:
            recipe_id = request.POST.get('recipe-id')
            list_id = request.POST.get('list-id')
            # get recipe and shopping list
            recipe_delete = Recipe.objects.get(recipe_id=recipe_id)
            shopping_list = ShoppingList.objects.get(id=list_id)
            # remove shopping list from recipe
            recipe_delete.shopping_lists.remove(shopping_list)
            return redirect('/list-details/'+str(list_id))
        # If user clicked to delete list
        elif 'delete-list' in request.POST:
            list_id = request.POST.get('list-id')
            ShoppingList.objects.get(id=list_id).delete()
            return redirect('/dashboard/')

#####################################################################################################



############################################# FUNCTIONS #############################################
def get_recipe_data(self,request):
    '''
    Get recipe data from post request
    '''
    recipe_id = request.POST.get('recipe-id')
    recipe_name = request.POST.get('recipe-name')
    recipe_image = request.POST.get('recipe-image')
    recipe_summary = request.POST.get('recipe-summary')
    recipe_instructions = request.POST.get('recipe-instructions')
    recipe_ingredients = request.POST.get('recipe-ingredients')
    recipe_dict = {
            'recipe_id': recipe_id,
            'recipe_name': recipe_name,
            'recipe_image': recipe_image,
            'recipe_summary': recipe_summary,
            'recipe_instructions': recipe_instructions,
            'recipe_ingredients': recipe_ingredients
    }

    return recipe_dict

def add_recipe(self, request, recipe_data):
    '''
    Add recipe to profile
    '''
    recipe_id = recipe_data.get('recipe_id')
    recipe_name = recipe_data.get('recipe_name')
    recipe_image = recipe_data.get('recipe_image')
    recipe_summary = recipe_data.get('recipe_summary')
    recipe_instructions = recipe_data.get('recipe_instructions')
    recipe_ingredients = recipe_data.get('recipe_ingredients')

    # Convert recipe ingredients to a dict
    recipe_ingredients = ast.literal_eval(recipe_ingredients)

    # If this recipe is not already added to profile AND the recipe is not in the database
    if (not Recipe.objects.filter(profile=self.request.user.profile, recipe_id=recipe_id)) and (not Recipe.objects.filter(recipe_id=recipe_id)):
        new_recipe = Recipe(recipe_id=recipe_id, name=recipe_name, image=recipe_image, summary=recipe_summary, instructions=recipe_instructions)
        new_recipe.save()
        new_recipe.profile.add(self.request.user.profile)
        for ing in recipe_ingredients:
            new_ingredient = Ingredient(ingredient_id=ing['id'], name=ing['name'], amount=ing['measures']['us']['amount'], measure_unit=ing['measures']['us']['unitLong'])
            new_ingredient.recipe = new_recipe
            new_ingredient.save()
        messages.success(request, f'Recipe Added!')
    # If this recipe is not already added to profile BUT the recipe is in the database
    elif (not Recipe.objects.filter(profile=self.request.user.profile, recipe_id=recipe_id)) and (Recipe.objects.filter(recipe_id=recipe_id)):
        update_recipe = Recipe.objects.get(recipe_id=recipe_id)
        update_recipe.profile.add(self.request.user.profile)
        messages.success(request, f'Recipe Added!')
    # Otherwise, the recipe has already been added to the account
    else:
        messages.warning(request, f'Recipe Has Already Been Added!')

def add_recipe_to_list(self, request, recipe_data, list_id):
    '''
    Add recipe to shopping list
    '''
    recipe_id = recipe_data.get('recipe_id')
    recipe_name = recipe_data.get('recipe_name')
    recipe_image = recipe_data.get('recipe_image')
    recipe_summary = recipe_data.get('recipe_summary')
    recipe_instructions = recipe_data.get('recipe_instructions')
    recipe_ingredients = recipe_data.get('recipe_ingredients')

    # If this recipe is not already added to the list
    if not (Recipe.objects.filter(profile=self.request.user.profile, recipe_id=recipe_id, shopping_lists__id=list_id)):
        recipe = Recipe.objects.get(profile=self.request.user.profile, recipe_id=recipe_id)
        recipe.shopping_lists.add(ShoppingList.objects.get(id=list_id))
        messages.success(request, f'Recipe Added!')
    # If this recipe is already in the list
    else:
        messages.warning(request, f'Recipe Has Already Been Added!')

def get_ingredients_in_recipe(self, request, recipe_data, list_id): 
    ingredient_data = []
    for recipe in recipe_data:
        new_ingredient = Ingredient.objects.filter(recipe=recipe)
        ingredient_data.append(new_ingredient)
    return ingredient_data
#####################################################################################################

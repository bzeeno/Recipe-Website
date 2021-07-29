from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, ShoppingList
import json
import spoonacular as sp

api = sp.API(settings.API_KEY)
# random_recipes = api.get_random_recipes(number=8)
f = open('results.json',)
random_recipes = json.load(f)

class Home(CreateView):
    template_name = 'home.html'

    def get(self, request):
        #request.session['recipes'] = random_recipes.json()
        request.session['recipes'] = random_recipes
        return render(request, self.template_name, request.session['recipes'])

    def post(self, request):
        # If post request is search
        if 'query' in request.POST:
            response = api.search_recipes_complex(query, number=8, addRecipeInformation=True, fillIngredients=True)
            f_data = response.json()
            context = {
                    'recipes': f_data['results']
            }
            return render(request, self.template_name, context)
        elif 'add-recipe' in request.POST:
            new_recipe = Recipe(recipe_id=request.POST.get('add-recipe'))
            new_recipe.save()
            new_recipe.profile.add(self.request.user.profile)
            messages.success(request, f'Recipe Added!')
            return render(request, self.template_name, request.session['recipes'])
        # If post request is load more
        elif 'load-more' in request.POST:
            response = api.get_random_recipes(number=8)
            data = response.json()
            for i in range(len(data['recipes'])):
                request.session['recipes']['recipes'].append(data['recipes'][i])
            return render(request, self.template_name, request.session['recipes'])

    def form_valid(self, form, request):
        if 'add-recipe' in request.POST:
            form.instance.profile = self.request.user
            return super().form_valid(form)


class RecipeDetailsView(TemplateView):
    template_name = 'recipe_detail.html'
    context_object_name = 'recipes'

    def get(self, request, **kwargs):
        recipe_id = self.kwargs['recipeid']
        response = api.get_recipe_information(recipe_id)
        recipe_data = response.json()

        context = {
                'recipe_data': recipe_data
        }
        return render(request, self.template_name, context)

class DashboardListView(ListView, LoginRequiredMixin):
    template_name = 'dashboard.html'
    recipe_list = [] 
    queryset = Recipe.objects.all()
    # Save 4 recipe ids to list to show in dashboard view
    #if len(Recipe.objects.all()) < 4:
    #    for recipe in Recipe.objects.all():
    #        recipe_list.append(recipe)
    #else:
    #    for recipe in Recipe.objects.all()[:4]:
    #        recipe_list.append(recipe)
    #print(recipe_list)
    #    
    def get_context_data(self, **kwargs):
        # Set context
        context = super(DashboardListView, self).get_context_data(**kwargs)
    #    #context['recipes'] = api.get_recipe_information_bulk(recipe_list)
    #    context['shopping_lists'] = ShoppingList.objects.all()
    #    print(context)
        return context

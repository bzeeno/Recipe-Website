from django.urls import path 
from django.urls import path, include
from . import views as recipe_views

urlpatterns = [ 
    path('', recipe_views.Home.as_view(), name='recipe-home'),
    path('dashboard/', recipe_views.DashboardListView.as_view(), name='dashboard'),
    path('recipe-list/', recipe_views.RecipeListView.as_view(), name='recipe-list'),
    path('recipe-list/<int:listid>', recipe_views.RecipeListView.as_view(), name='recipe-list'),
    path('recipe-details/<int:recipeid>', recipe_views.RecipeDetailsView.as_view(), name='recipe-details'),
    path('list-details/<int:listid>', recipe_views.ShoppingListDetailsView.as_view(), name='list-details'),
    path('create-list/', recipe_views.CreateListView.as_view(), name='create-list'),
    path('shopping-lists/', recipe_views.ShoppingListsView.as_view(), name='shopping-lists'),
]

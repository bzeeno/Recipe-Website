from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views as user_views

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('profile-settings/', user_views.profile_settings, name='profile-settings'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

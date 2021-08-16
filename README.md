# Recipe-Website
Website for keeping track of recipes and their ingredients. Project uses Django and PostgreSQL and is deployed on heroku

Table of Contents
=================

   * [Introduction](#introduction)
   * [Directory Structure](#directory-structure)

## Introduction
This application is intended to make organizing shopping lists easier. The website utilizes the Spoonacular API to get recipe information. 
The home page displays 8 random recipes and allows users to search for recipes with the search bar. If the user is logged in, they can add recipes to their account.
Doing so will now associate that recipe with the user's account. From there, the user can create shopping lists on their dashboard, and add recipes to their lists.
The ingredients from all the recipes in the shopping list will be displayed to the user.

## Directory Structure
<pre>
├── manage.py
├── Procfile
├── requirements.txt
├── config
│   ├── ...
│   ├── settings.py
│   └── urls.py
├── frontend
│   ├── ...
│   ├── src
│   │   ├── ...
│   ├── static
│   │   ├── ...
│   │   ├── css
│   │       └── main.css
│   ├── templates
│   │   └── frontend
│   │       ├── base.html
│   │       ├── create_list.html
│   │       ├── dashboard.html
│   │       ├── home.html
│   │       ├── list_detail.html
│   │       ├── recipe_detail.html
│   │       ├── recipe_list.html
│   │       ├── shopping_lists.html
│   │       └── users
│   │           ├── dashboard.html
│   │           ├── login.html
│   │           ├── logout.html
│   │           ├── profile-settings.html
│   │           └── register.html
├── recipe
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── mixins.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── users
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── __init__.py
    ├── models.py
    ├── signals.py
    ├── tests.py
    ├── urls.py
    └── views.py
</pre>

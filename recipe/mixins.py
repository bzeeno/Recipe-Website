from django.conf import settings
import json
import spoonacular as sp

api = sp.API(settings.API_KEY)

class APIMixin:
    def __init__(self, *args, **kwargs):
        self.type
        
    response = api.get_random_recipes(number=1)
    data = response.json()
    json_obj = json.dumps(data)

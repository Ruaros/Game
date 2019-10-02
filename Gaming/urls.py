from django.urls import path
from .views import *

urlpatterns = [
    path('',         TagCreate.as_view(), name = "yours_name"),
    path('choise/',  choise_name,         name = "choise_name"),
    path('game/',    game_it,             name = "game_page"),  
    path('setings/', setings,             name = "setings_url"),
    path('add/',     add_action,          name = "add_action_url"),
    path('adding/',  adding_action,       name = "adding_action_url"),
    path('change/',  change_action,       name = "change_action_url"),
    #url(r'^$',       home,                name = 'home'),
    path(r'^dtny',    dtny,                name = 'dtny'),
        
    ]

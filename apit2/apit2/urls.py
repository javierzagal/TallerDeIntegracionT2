"""apit2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index),
    #path('car', views.add_car),
    #path('<str:car_name>',views.get_car),
    #CREAR
    path('leagues',views.leagues), #POST Y GET
    path('leagues/<str:league_id>', views.league),
    path('leagues/<str:league_id>/teams',views.teamInLeague),#POST y GET
    #path('teams/<str:team_id>/players',views.add_player),
    #OBTENER
    path('teams', views.teams), #retorna todos los equipos
    path('teams/<str:team_id>', views.team),
    path('teams/<str:team_id>/players', views.playerInTeam),
    path('players', views.players),
    path('players/<str:player_id>', views.player),

    #ENTRENAR
    path('players/<str:player_id>/train', views.trainPlayer),
    path('teams/<str:team_id>/train', views.trainTeam),
    path('leagues/<str:league_id>/train', views.trainLeague),
    #path('leagues/<str:league_id>',views.get_league),

]

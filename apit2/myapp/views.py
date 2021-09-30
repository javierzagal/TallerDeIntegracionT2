from django.http.response import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

from base64 import b64encode

from myapp.models import Car, League, Team, Player
from myapp.serializers import LeagueSerializer, TeamSerializer, PlayerSerializer

baseurl = ''
def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

#def get_car(request, car_name):
#    if request.method == 'GET':
#        try:
#            car = Car.objects.get(name=car_name)
#            response = json.dumps([{ 'Car': car.name, 'Top Speed': car.top_speed}])
#        except:
#            response = json.dumps([{ 'Error': 'No car with that name'}])
#    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def add_car(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        car_name = payload['car_name']
        top_speed = payload['top_speed']
        car = Car(name=car_name, top_speed=top_speed)
        try:
            car.save()
            response = json.dumps([{ 'Success': 'Car added successfully!'}])
        except:
            response = json.dumps([{ 'Error': 'Car could not be added!'}])
    return HttpResponse(response, content_type='text/json')



#/leagues
# Ver todas las ligas (GET) / Agregar liga (POST)
@csrf_exempt
@api_view(['GET','POST'])
def leagues(request): #Ver todas las ligas/ Agregar liga
    if request.method == 'POST':
        payload = json.loads(request.body)
        league_name = payload['name']
        league_sport = payload['sport']
        idstring = league_name + ":" + league_sport
        id_team = b64encode(idstring.encode()).decode('utf-8')[0:22]
        this_id = id_team

        league_teams = baseurl + '/leagues/'+ this_id + '/teams'
        league_players = baseurl + '/leagues/'+ this_id + '/players'
        league = League(id = this_id, name=league_name, sport=league_sport, teams=league_teams, players=league_players, self_name=baseurl + '/leagues/' +  this_id)
        try:
            league.save()
            response = json.dumps([{ 'Success': 'League added successfully!'}])
        except:
            response = json.dumps([{ 'Error': 'League could not be added!'}])
    
    elif request.method == 'GET':
        try:
            leagues = League.objects.all()
            serializer = LeagueSerializer(leagues, many=True)
            return Response(serializer.data)
            #qs_json = serializers.serialize('json',leagues)
            #response = qs_json

        except:
            response = json.dumps([{ 'Error': 'No leagues'}])
    return HttpResponse(response, content_type='text/json')  

#leagues/id
# Ver liga por su id (GET)
@api_view(['GET'])
def league(request, league_id):
    if request.method == 'GET':
        try:
            league = League.objects.get(pk = league_id)
            serializer = LeagueSerializer(league, many=False)
            return Response(serializer.data)
            #response = json.dumps([{ 'id': league.name, 'name': league.sport, 'teams': league.teams, 'players': league.players, 'self': league.players}])
        except:
            response = "liga no encontrada"
    return HttpResponse(response, content_type='text/json')  

#leagues/id/teams
#Obtener todos los equipos de la liga (GET)/Crear un equipo (POST)
@csrf_exempt
@api_view(['GET','POST'])
def teamInLeague(request,league_id):
    if request.method == 'POST':
        try: 
            League.objects.get(pk = league_id)
            
            payload = json.loads(request.body)
            team_name = payload['name']
            team_city  = payload['city']
            idstring = team_name + ":" + team_city
            id_team = b64encode(idstring.encode()).decode('utf-8')[0:22]
            this_id = id_team


            team_league = baseurl + '/leagues/'+ league_id
            team_players = baseurl + '/teams/'+ this_id + '/players'
            team_self = baseurl + '/teams/'+ this_id


            team = Team(id= this_id, league_id= league_id, name=team_name, city=team_city,
             league= team_league, players=team_players,self_name= team_self)
            try:
                team.save()
                response = json.dumps([{ 'Success': 'Team added successfully!'}])
            except:
                response = json.dumps([{ 'Error': 'Team could not be added!'}])
        except:
            response = json.dumps([{ 'Error': 'League does not exist!'}])
    
    
    elif request.method == 'GET':
        try:
            #League.objects.get(pk = league_id)

            teams = Team.objects.filter(league_id = league_id)
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)
        except:
            response = json.dumps([{ 'Error': 'League does not exist!'}])
            return HttpResponseNotFound()


    return HttpResponse(response, content_type='text/json')  


#TEAMS
#/teams
def teams(request):
    if request.method == 'GET':
        response = serializers.serialize('json',Team.objects.all()) 
    return HttpResponse(response, content_type='text/json')  


def team(request,team_id):
    if request.method == 'GET':
        try:
            team = Team.objects.get(pk = team_id)
            response = json.dumps([{ 'id': team_id, 'league_id': team.league_id, 'name': team.name, 'city': team.city, 'league': team.league, 'players': team.players, 'self': team.self}])
            return HttpResponse(response, content_type='text/json')  
        except:
            response = "404 equipo no encontrado"
            return HttpResponseNotFound()

@csrf_exempt
@api_view(['GET','POST'])
def playerInTeam(request,team_id):
    if request.method == 'POST':
        try: 
            league_id = str(Team.objects.get(id = team_id))
      
            payload = json.loads(request.body)
            player_name = payload['name']
            player_age  = int(payload['age'])
            player_position = payload['position']

            idstring = player_name + ":" + player_position
            this_id = b64encode(idstring.encode()).decode('utf-8')[0:22]

            player_league = baseurl + '/leagues/'+ league_id
            player_team = baseurl + '/teams/' + team_id
            player_self = baseurl + '/players/' + this_id

            player = Player(id= this_id, team_id= team_id, name=player_name, age= int(player_age), position= player_position, 
            times_trained= 0, league=player_league, team=player_team, self_name=player_self)
            try:
                player.save()
                response = json.dumps([{ 'Success': 'Player added successfully!'}])
            except:
                response = json.dumps([{ 'Error': 'Player could not be added!'}])
                #YA EXISTE EL JUGADOR
                return HttpResponse(200)

        except:
            response = json.dumps([{ 'Error': 'Team does not exist!'}])
    
    
    elif request.method == 'GET':
        try:
            print("l")
            print(Player.objects.filter(team_id = team_id))
            players = Player.objects.filter(team_id = team_id)
            serializer = PlayerSerializer(players, many=True)
            return Response(serializer.data)

        except:
            response = json.dumps([{ 'Error': 'League does not exist!'}])
            return HttpResponseNotFound()


    return HttpResponse(response, content_type='text/json')  


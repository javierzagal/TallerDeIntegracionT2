from django.http.response import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base64 import b64encode
from rest_framework.views import exception_handler
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
        try:
            league_name = payload['name']
            league_sport = payload['sport']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            payload['id']
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        idstring = league_name + ":" + league_sport

        id_team = b64encode(idstring.encode()).decode('utf-8')[0:22]
        this_id = id_team
        try:
            ligaExistente = League.objects.get(pk = id_team) 
            serializer = LeagueSerializer(ligaExistente, many= False)
            return Response(serializer.data,status=status.HTTP_409_CONFLICT)
        except:
            league_teams = baseurl + '/leagues/'+ this_id + '/teams'
            league_players = baseurl + '/leagues/'+ this_id + '/players'
            league = League(id = this_id, name=league_name, sport=league_sport, teams=league_teams, players=league_players, self_name=baseurl + '/leagues/' +  this_id)
            try:
                league.save()
                serializer = LeagueSerializer(League.objects.get(pk = this_id), many= False)
                return Response(serializer.data,status=status.HTTP_201_CREATED)

            except:
                response = json.dumps([{ 'Error': 'League could not be added!'}])
    
    elif request.method == 'GET':
        try:
            leagues = League.objects.all()
            serializer = LeagueSerializer(leagues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            response = json.dumps([{ 'Error': 'No leagues'}])
    return HttpResponse(response, content_type='text/json')  

#leagues/id
# Ver liga por su id (GET)
@api_view(['GET', 'DELETE'])
def league(request, league_id):
    if request.method == 'GET':
        try:
            league = League.objects.get(pk = league_id)
            serializer = LeagueSerializer(league, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        try:
            league = League.objects.get(pk = league_id)
            try:
                teams = Team.objects.filter(league_id = league_id)
                for team in teams:
                    players = Player.objects.filter(team_id = team.id)
                    for player in players:
                        deleteThisPlayer(player.id)
                    team.delete()
            except:
                pass
            league.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except:
            return HttpResponseNotFound()

#leagues/id/teams CREAR EQUIPO
#Obtener todos los equipos de la liga (GET)/Crear un equipo (POST)
@csrf_exempt
@api_view(['GET','POST'])
def teamInLeague(request,league_id):
    if request.method == 'POST':
        try: 
            League.objects.get(pk = league_id)
        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY) #liga no existe

        payload = json.loads(request.body)
        try:
            team_name = payload['name']
            team_city  = payload['city']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        try:
            payload["id"]
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        except:
            pass
        
        idstring = team_name + ":" + team_city
        id_team = b64encode(idstring.encode()).decode('utf-8')[0:22]
        this_id = id_team
        try:
            teamExistente = Team.objects.get(pk = this_id)
            serializer = TeamSerializer(teamExistente, many= False)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)
            # team ya existe
        except:
            pass

        team_league = baseurl + '/leagues/'+ league_id
        team_players = baseurl + '/teams/'+ this_id + '/players'
        team_self = baseurl + '/teams/'+ this_id


        team = Team(id= this_id, league_id= league_id, name=team_name, city=team_city,
            league= team_league, players=team_players,self_name= team_self)
        try:
            team.save()
            return Response(TeamSerializer(team,many=False).data,status=status.HTTP_201_CREATED)
        except:
            response = json.dumps([{ 'Error': 'Team could not be added!'}])

    
    
    elif request.method == 'GET':
        try:
            League.objects.get(pk = league_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            teams = Team.objects.filter(league_id = league_id)
            if teams == []:
                return HttpResponseNotFound()
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return HttpResponseNotFound()


    return HttpResponse(response, content_type='text/json')  
@api_view(['GET'])
def playersInLeague(request,league_id):
    if request.method == 'GET':
        try:
            League.objects.get(pk = league_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        league_link = "/leagues/" + league_id
        players = Player.objects.filter(league = league_link)
        serializer = PlayerSerializer(players,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


#TEAMS
#/teams
@api_view(['GET'])
def teams(request): #show all teams
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


@api_view(['GET','DELETE'])
def team(request,team_id):
    if request.method == 'GET':
        try:
            team = Team.objects.get(pk = team_id)
            serializer = TeamSerializer(team, many=False)
            return Response(serializer.data)
        except:
            return HttpResponseNotFound()
    elif request.method == 'DELETE':
        try:
            team = Team.objects.get(pk = team_id)
            #primero borrar jugadores
            try:
                playersInThisTeam = Player.objects.filter(team_id = team_id)
                for player in playersInThisTeam:
                    deleteThisPlayer(player.id) 
            except:
                pass
            #borrar este team
            team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except:
            return HttpResponseNotFound() #no se encontro el team

#teams/id/players
@csrf_exempt
@api_view(['GET','POST','DELETE'])
def playerInTeam(request,team_id):
    if request.method == 'POST':
        try:
            Team.objects.get(pk = team_id)
        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try: 
            league_id = str(Team.objects.get(pk = team_id))
      
            payload = json.loads(request.body)
            try:
                player_name = payload['name']
                player_age  = int(payload['age'])
                player_position = payload['position']
                if len(payload) > 3:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                payload['id']
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            idstring = player_name + ":" + player_position
            this_id = b64encode(idstring.encode()).decode('utf-8')[0:22]

            player_league = baseurl + '/leagues/'+ league_id
            player_team = baseurl + '/teams/' + team_id
            player_self = baseurl + '/players/' + this_id

            player = Player(id= this_id, team_id= team_id, name=player_name, age= int(player_age), position= player_position, 
            times_trained= 0, league=player_league, team=player_team, self_name=player_self)
            try:
                existingplayer = Player.objects.get(pk = this_id)
                serializer = PlayerSerializer(existingplayer, many= False)
                return Response(serializer.data,status=status.HTTP_409_CONFLICT)
                #jugador ya existe
            except:
                player.save()
                serializer = PlayerSerializer(player,many=False)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
                #jugador creado


        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            # team no existe
    
    
    elif request.method == 'GET':
        try:
            Team.objects.get(pk = team_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            players = Player.objects.filter(team_id = team_id)
            serializer = PlayerSerializer(players, many=True)
            return Response(serializer.data)

        except:
            return HttpResponseNotFound()
#/players   
@csrf_exempt
@api_view(['GET'])
def players(request):
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
        
#/players/id
@csrf_exempt
@api_view(['GET','DELETE'])
def player(request,player_id):
    if request.method == 'GET':
        try:
            player = Player.objects.get(pk = player_id)
            serializer = PlayerSerializer(player, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            #not found
            return HttpResponseNotFound()
    elif request.method == 'DELETE':
        try:
            deleteThisPlayer(player_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            #not found
            return HttpResponseNotFound()

@csrf_exempt
@api_view(['PUT'])
def trainPlayer(request,player_id):
    if request.method == 'PUT':
        try:
            trainThisPlayer(player_id)
            return HttpResponse(200)
        except:
            #not found
            return HttpResponseNotFound()

@csrf_exempt
@api_view(['PUT'])
def trainTeam(request,team_id):
    if request.method == 'PUT':
        try:
            trainThisTeam(team_id)
            return HttpResponse(200)
        except:
            #not found
            return HttpResponseNotFound()

@csrf_exempt
@api_view(['PUT'])
def trainLeague(request,league_id):
    if request.method == 'PUT':
        try:
            TeamsInThisLeague = Team.objects.filter(league_id = league_id)
            for team in TeamsInThisLeague:
                trainThisTeam(team.id)
            return HttpResponse(200)
        except:
            #not found
            return HttpResponseNotFound()


# Funciones para borrar efectos cascadas

def deleteThisPlayer(id):
    player = Player.objects.get(pk = id)
    player.delete()


def trainThisTeam(id):
    playersInThisTeam = Player.objects.filter(team_id = id)
    for player in playersInThisTeam:
        trainThisPlayer(player.id)

def trainThisPlayer(id):
    player = Player.objects.get(pk = id)
    player.times_trained += 1
    player.save()
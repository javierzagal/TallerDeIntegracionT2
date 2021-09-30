from rest_framework import serializers
from .models import League, Team, Player
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = 'id','name','sport','teams','players','self'
LeagueSerializer._declared_fields["self"] = serializers.CharField(source = "self_name")

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = 'id','league_id','name','city','league','players','self'
TeamSerializer._declared_fields["self"] = serializers.CharField(source = "self_name")

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = 'id','team_id','name','age','position','times_trained','league','team','self'
TeamSerializer._declared_fields["self"] = serializers.CharField(source = "self_name")
from django.db import models

# Create your models here.
#ids are generated automatically by django
class Car(models.Model):
    name = models.CharField(max_length = 100)
    top_speed = models.IntegerField()

class League(models.Model):
    id = models.CharField(max_length = 100,primary_key=True)
    name = models.CharField(max_length = 100)
    sport = models.CharField(max_length = 100)

    teams = models.CharField(max_length = 100)
    players = models.CharField(max_length = 100)
    self_name = models.CharField(db_column= 'self', max_length = 100)
    
    class Meta:
        verbose_name = 'League'
        verbose_name_plural = 'League'


    def __str__(self):
        return self.name





class Team(models.Model):
    id = models.CharField(max_length = 100,primary_key=True)
    league_id = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)

    league = models.CharField(max_length = 100)
    players = models.CharField(max_length = 100)
    self_name = models.CharField(max_length = 100)
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Team'


    def __str__(self):
        return self.league_id

class Player(models.Model):
    id = models.CharField(max_length = 100,primary_key=True)
    team_id = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    age = models.IntegerField()
    position = models.CharField(max_length = 100)
    times_trained = models.IntegerField()

    league = models.CharField(max_length = 100)
    team = models.CharField(max_length = 100)
    self_name = models.CharField(max_length = 100)
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Player'


    def __str__(self):
        return self.name
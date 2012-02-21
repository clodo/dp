from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 50)

class Team(models.Model):
    name = models.CharField(max_length = 50)

class Fixture(models.Model):
    date = models.DateField()

class Match(models.Model):
    local_team = models.ForeignKey(Team, related_name = "local_team")
    visitor_team = models.ForeignKey(Team, related_name = "visitor_team")
    fixture = models.ForeignKey(Fixture)


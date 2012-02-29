from django.db import models
from datetime import datetime

class User(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

    def set_match_result(self, match, local_goals, visitor_goals):
        UserMatchResult.objects.create(user = self,
                                       match = match, 
                                       local_goals = local_goals, 
                                       visitor_goals = visitor_goals)

class Team(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Equipo"

class Fixture(models.Model):
    date = models.DateField(verbose_name = "Fecha")
    name = models.CharField(max_length = 50, default = str(datetime.now().date()))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-date']

    @staticmethod
    def get_current():
        return Fixture.objects.all()[0]


class Match(models.Model):
    local_team = models.ForeignKey(Team, related_name = "local_team", verbose_name = "Equipo Local")
    visitor_team = models.ForeignKey(Team, related_name = "visitor_team", verbose_name = "Equipo Visitante")
    fixture = models.ForeignKey(Fixture)
    local_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Local Goles")
    visitor_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Visitante Goles")

    def __unicode__(self):
        return "%s - %s | %s vs %s " % (self.fixture.date, self.fixture.name, self.local_team.name, self.visitor_team.name)

    class Meta:
        verbose_name = "Partido"

class UserMatchResult(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    local_goals = models.PositiveIntegerField()
    visitor_goals = models.PositiveIntegerField()


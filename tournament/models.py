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
    def get_finished_matches(self):
        return [usermatchresult.match 
                for usermatchresult in self.usermatchresult_set.all() 
                if usermatchresult.match.finished]
        

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

    def get_finished_matches(self):
        return self.match_set.filter(finished = True)

    class Meta:
        ordering = ['-date']

    @staticmethod
    def get_current():
        return Fixture.objects.all()[0]


class Match(models.Model):
    local_team = models.ForeignKey(Team, related_name = "local_team", verbose_name = "Equipo Local")
    visitor_team = models.ForeignKey(Team, related_name = "visitor_team", verbose_name = "Equipo Visitante")
    fixture = models.ForeignKey(Fixture)
    local_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Local Goles", default = 0)
    visitor_team_goals = models.PositiveIntegerField(verbose_name = "Equipo Visitante Goles", default = 0)
    finished = models.BooleanField(verbose_name = "Terminado", default = False)

    def __unicode__(self):
        return "%s - %s | %s vs %s " % (self.fixture.date, self.fixture.name, self.local_team.name, self.visitor_team.name)

    class Meta:
        verbose_name = "Partido"

class UserMatchResult(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    local_goals = models.PositiveIntegerField()
    visitor_goals = models.PositiveIntegerField()


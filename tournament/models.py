from django.db import models
from datetime import datetime
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

    def set_match_result(self, match, local_team_goals, visitor_team_goals):
        UserMatchPrediction.objects.create(user = self,
                                       match = match, 
                                       local_team_goals = local_team_goals, 
                                       visitor_team_goals = visitor_team_goals)

    def get_points(self):
        return sum([user_prediction.get_points() for user_prediction in self.usermatchprediction_set.all() 
                    if user_prediction.match.finished])
        

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

    def get_finished_matchs(self):
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
    is_classic = models.BooleanField(verbose_name = "Clasico", default = False)

    def __unicode__(self):
        return "%s - %s | %s vs %s " % (self.fixture.date, self.fixture.name, self.local_team.name, self.visitor_team.name)

    class Meta:
        verbose_name = "Partido"

class UserMatchPrediction(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    local_team_goals = models.PositiveIntegerField()
    visitor_team_goals = models.PositiveIntegerField()
    is_double = models.BooleanField(verbose_name = "Doble", default = False)

    def is_a_moral_prediction(self):
        prediction_local_team_had_won = self.__class__.has_local_team_won(self.local_team_goals, self.visitor_team_goals)
        match_local_team_had_won = self.__class__.has_local_team_won(self.match.local_team_goals, self.match.visitor_team_goals)

        return prediction_local_team_had_won == match_local_team_had_won

    def is_a_exact_prediction(self):
        return self.match.local_team_goals == self.local_team_goals and  \
               self.match.visitor_team_goals == self.visitor_team_goals

    def get_points(self):
        points = 0
        if self.is_a_exact_prediction():
            points = settings.POINTS['exact']
        elif self.is_a_moral_prediction():
            points = settings.POINTS['moral']

        if self.match.is_classic:
            points *= settings.POINTS['classic']

        if self.is_double:
            points *= settings.POINTS['double']

        return points


    @classmethod
    def has_local_team_won(cls, local_team_goals, visitor_team_goals):
        return None if visitor_team_goals == local_team_goals else (visitor_team_goals < local_team_goals)



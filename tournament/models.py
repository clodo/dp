from django.db import models
from datetime import datetime

class User(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

    def set_match_result(self, match, local_team_goals, visitor_team_goals):
        UserMatchPrediction.objects.create(user = self,
                                       match = match, 
                                       local_team_goals = local_team_goals, 
                                       visitor_team_goals = visitor_team_goals)

    def get_predictions_of_finished_matchs(self):
        return [user_prediction for user_prediction in self.usermatchprediction_set.all() 
                if user_prediction.match.finished]
    
    def get_good_predictions(self):
        return [prediction for prediction in self.get_predictions_of_finished_matchs() 
                if prediction.match.local_team_goals == prediction.local_team_goals and
                   prediction.match.visitor_team_goals == prediction.visitor_team_goals]

    def get_points(self):
        return len(self.get_good_predictions()) * 2
        

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

    def __unicode__(self):
        return "%s - %s | %s vs %s " % (self.fixture.date, self.fixture.name, self.local_team.name, self.visitor_team.name)

    class Meta:
        verbose_name = "Partido"

class UserMatchPrediction(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    local_team_goals = models.PositiveIntegerField()
    visitor_team_goals = models.PositiveIntegerField()


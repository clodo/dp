from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 50)

    def set_match_result(self, match, local_goals, visitor_goals):
        UserMatchResult.objects.create(user = self,
                                       match = match, 
                                       local_goals = local_goals, 
                                       visitor_goals = visitor_goals)


class Team(models.Model):
    name = models.CharField(max_length = 50)

class Fixture(models.Model):
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    @staticmethod
    def get_current():
        return Fixture.objects.all()[0]


class Match(models.Model):
    local_team = models.ForeignKey(Team, related_name = "local_team")
    visitor_team = models.ForeignKey(Team, related_name = "visitor_team")
    fixture = models.ForeignKey(Fixture)

class UserMatchResult(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    local_goals = models.PositiveIntegerField()
    visitor_goals = models.PositiveIntegerField()


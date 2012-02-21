from django.test import TestCase
from tournament.models import Team, Fixture, Match
from datetime import datetime

class TournamentTest(TestCase):

    def test_set_current_fixture(self):
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")
        fixture = Fixture.objects.create(date = datetime.now())

        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = fixture)

        self.assertEqual(len(fixture.match_set.all()), 1)

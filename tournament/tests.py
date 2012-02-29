from django.test import TestCase
from tournament.models import Team, Fixture, Match, User
from datetime import datetime, timedelta

class TournamentTest(TestCase):

    def test_set_current_fixture(self):
        # Teams
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")

        # Fixtures
        fixture = Fixture.objects.create(date = datetime.now())

        # Matches
        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = fixture)

        self.assertEqual(len(fixture.match_set.all()), 1)

    def test_get_current_fixture(self):
        # Teams
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")
        team_c = Team.objects.create(name = "Team C")

        # Fixtures
        current_fixture = Fixture.objects.create(date = datetime.now())
        past_fixture = Fixture.objects.create(date = (datetime.now() - timedelta(weeks = 1)))

        # Matches
        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = current_fixture)

        match = Match.objects.create(local_team = team_c, 
                                     visitor_team = team_b,
                                     fixture = past_fixture)

        match = Match.objects.create(local_team = team_c, 
                                     visitor_team = team_a,
                                     fixture = past_fixture)

        self.assertEqual(Fixture.get_current().id, current_fixture.id)

    def test_user_set_fixtures_results(self):
        # Teams
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")

        # Fixtures
        fixture = Fixture.objects.create(date = datetime.now())

        # Matches
        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = fixture)
        # User
        user = User.objects.create(name = "User")
        user.set_match_result(match, 0, 0)

        self.assertEqual(len(user.usermatchresult_set.all()), 1)



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

        # Matchs
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

        self.assertEqual(Fixture.get_current().id, current_fixture.id)

    def test_user_set_fixtures_results(self):
        # Teams
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")

        # Fixtures
        fixture = Fixture.objects.create(date = datetime.now())

        # Matchs
        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = fixture)
        # User
        user = User.objects.create(name = "User")
        user.set_match_result(match, 0, 0)

        self.assertEqual(len(user.usermatchresult_set.all()), 1)

    def test_get_fixture_finished_matchs(self):
        # Teams
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")
        team_c = Team.objects.create(name = "Team C")
        team_f = Team.objects.create(name = "Team F")

        # Fixtures
        fixture = Fixture.objects.create(date = datetime.now())

        # Matchs
        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = fixture)

        match = Match.objects.create(local_team = team_c, 
                                     visitor_team = team_f,
                                     fixture = fixture, 
                                     finished = True)

        match = Match.objects.create(local_team = team_c, 
                                     visitor_team = team_a,
                                     fixture = fixture,
                                     finished = True)

        self.assertEqual(fixture.get_finished_matchs().count(), 2)

    def test_get_user_finished_matchs(self):
        # Teams
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")
        team_c = Team.objects.create(name = "Team C")
        team_f = Team.objects.create(name = "Team F")

        # Fixtures
        fixture = Fixture.objects.create(date = datetime.now())

        # Matchs
        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = fixture)

        match_1 = Match.objects.create(local_team = team_c, 
                                     visitor_team = team_f,
                                     fixture = fixture, 
                                     finished = True)

        match_2 = Match.objects.create(local_team = team_c, 
                                     visitor_team = team_a,
                                     fixture = fixture)
        # User
        user = User.objects.create(name = "User")
        user.set_match_result(match, 2, 0)
        user.set_match_result(match_1, 1, 0)
        user.set_match_result(match_2, 2, 0)

        self.assertEqual(len(user.get_predictions_of_finished_matchs()), 1)

    def test_assert_user_predictions_with_real_scores(self):
        # Teams
        team_a = Team.objects.create(name = "Team A")
        team_b = Team.objects.create(name = "Team B")
        team_c = Team.objects.create(name = "Team C")
        team_f = Team.objects.create(name = "Team F")

        # Fixtures
        fixture = Fixture.objects.create(date = datetime.now())

        # Matchs
        match = Match.objects.create(local_team = team_a, 
                                     visitor_team = team_b,
                                     fixture = fixture,
                                     finished = True, 
                                     visitor_team_goals = 0, 
                                     local_team_goals = 2)

        match_1 = Match.objects.create(local_team = team_c, 
                                       visitor_team = team_f,
                                       fixture = fixture, 
                                       finished = True,
                                       visitor_team_goals = 0,
                                       local_team_goals = 2)
  
        match_2 = Match.objects.create(local_team = team_c, 
                                       visitor_team = team_a,
                                       fixture = fixture, 
                                       finished = True,
                                       visitor_team_goals = 0,
                                       local_team_goals = 0)
  
        # User
        user = User.objects.create(name = "User")
        user.set_match_result(match, 2, 0)
        user.set_match_result(match_1, 1, 0)
        user.set_match_result(match_2, 0, 0)

        self.assertEqual(len(user.get_good_predictions()), 2)

from django.test import TestCase
from datetime import datetime, timedelta
from tournament.models import Team, Fixture, Match, User
from tournament.tests.factories import *

class TournamentTest(TestCase):

    def test_setting_current_fixture(self):
        # Fixtures
        fixture = FixtureFactory()

        # Matchs
        match = MatchFactory(fixture = fixture)

        self.assertEqual(len(fixture.match_set.all()), 1)

    def test_gettting_the_current_fixture(self):
        # Fixtures
        current_fixture = FixtureFactory()
        past_fixture = FixtureFactory(date = (datetime.now() - timedelta(weeks = 1)))

        self.assertEqual(Fixture.get_current().id, current_fixture.id)

    def test_the_user_setting_fixtures_results(self):
        # Fixtures
        fixture = FixtureFactory()

        # Matchs
        match = MatchFactory(fixture = fixture)

        # User
        user = UserFactory()
        user.set_match_result(match, 0, 0)

        self.assertEqual(len(user.usermatchprediction_set.all()), 1)

    def test_gettting_fixtures_finished_matchs(self):
        # Fixtures
        fixture = FixtureFactory()

        # Matchs
        match = MatchFactory(fixture = fixture)
        match = MatchFactory(fixture = fixture, finished = True)
        match = MatchFactory(fixture = fixture, finished = True)

        self.assertEqual(fixture.get_finished_matchs().count(), 2)

    def test_getting_the_users_finished_matchs(self):
        # Fixtures
        fixture = Fixture.objects.create(date = datetime.now())

        # Matchs
        match = MatchFactory(fixture = fixture)
        match_1 = MatchFactory(fixture = fixture, finished = True)
        match_2 = MatchFactory(fixture = fixture)

        # User
        user = UserFactory()
        user.set_match_result(match, 2, 0)
        user.set_match_result(match_1, 1, 0)
        user.set_match_result(match_2, 2, 0)

        self.assertEqual(len(user.get_predictions_of_finished_matchs()), 1)

    def test_the_user_exact_predictions(self):
        # Fixtures
        fixture = FixtureFactory()

        # Matchs
        match = MatchFactory(fixture = fixture,
                             finished = True, 
                             visitor_team_goals = 0, 
                             local_team_goals = 2)

        match_1 = MatchFactory(fixture = fixture, 
                               finished = True,
                               visitor_team_goals = 0,
                               local_team_goals = 2)
  
        match_2 = MatchFactory(fixture = fixture, 
                               finished = True,
                               visitor_team_goals = 0,
                               local_team_goals = 0)
  
        # User
        user = UserFactory()
        user.set_match_result(match, 2, 0)
        user.set_match_result(match_1, 1, 0)
        user.set_match_result(match_2, 0, 0)

        self.assertEqual(len(user.get_good_exact_predictions()), 2)
        self.assertEqual(user.get_points(), 4)

    def test_users_moral_predictions(self):
        # Match 1 - is moral prediction
        match = MatchFactory()

        user_prediction_local_team_win = \
            UserMatchPredictionFactory(visitor_team_goals = match.visitor_team_goals, 
                                       local_team_goals = match.local_team_goals, 
                                       match = match)


        self.assertTrue(user_prediction_local_team_win.is_a_moral_prediction())

        # Match 2 - is moral prediction
        match = MatchFactory(visitor_team_goals = 2, 
                             local_team_goals = 0)

        user_prediction_local_team_lose = \
            UserMatchPredictionFactory(visitor_team_goals = match.visitor_team_goals, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertTrue(user_prediction_local_team_lose.is_a_moral_prediction())

        # Match 3 - is moral prediction
        match = MatchFactory(visitor_team_goals = 0, 
                             local_team_goals = 0)

        user_prediction_local_team_draw = \
            UserMatchPredictionFactory(visitor_team_goals = match.visitor_team_goals, 
                                       local_team_goals = match.local_team_goals, 
                                       match = match)

        self.assertTrue(user_prediction_local_team_draw.is_a_moral_prediction())

        # Match 4 - is not moral prediction
        match = MatchFactory(visitor_team_goals = 0, 
                             local_team_goals = 0)

        user_prediction_local_team_draw = \
            UserMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 1, 
                                       match = match)

        self.assertFalse(user_prediction_local_team_draw.is_a_moral_prediction())

        user_prediction_local_team_draw = \
            UserMatchPredictionFactory(visitor_team_goals = 1, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertFalse(user_prediction_local_team_draw.is_a_moral_prediction())

        # Match 5 - is not moral prediction
        match = MatchFactory(visitor_team_goals = 1, 
                             local_team_goals = 2)

        user_prediction_local_team_draw = \
            UserMatchPredictionFactory(visitor_team_goals = 0, 
                                       local_team_goals = 0, 
                                       match = match)

        self.assertFalse(user_prediction_local_team_draw.is_a_moral_prediction())


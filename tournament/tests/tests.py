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

    def test_users_exact_predictions(self):
        # Matchs
        match_1 = MatchFactory()
        match_2 = MatchFactory()

        # Predictions
        prediction_match_1_true = UserMatchPredictionFactory(visitor_team_goals = match_1.visitor_team_goals, 
                                                        local_team_goals = match_1.local_team_goals, 
                                                        match = match_1)

        prediction_match_2_false = UserMatchPredictionFactory(visitor_team_goals = (match_2.visitor_team_goals + 1), 
                                                        local_team_goals = match_2.local_team_goals, 
                                                        match = match_2)


        self.assertTrue(prediction_match_1_true.is_a_exact_prediction())
        self.assertFalse(prediction_match_2_false.is_a_exact_prediction())

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

    def test_get_user_points_from_one_correct_exact_prediction(self):
        user = UserFactory()
        match = MatchFactory(finished = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        self.assertEqual(3, user.get_points())

    def test_get_user_points_from_some_exact_prediction_and_some_not(self):
        user = UserFactory()
        match = MatchFactory(finished = True, visitor_team_goals = 2, local_team_goals = 0)
        match_2 = MatchFactory(finished = True, visitor_team_goals = 0, local_team_goals = 2)

        match_prediction_true = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        match_prediction_false = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 2)

        match_prediction_2_false = \
                UserMatchPredictionFactory(match = match_2,
                                           user = user, 
                                           visitor_team_goals = 2,
                                           local_team_goals = 0)


        self.assertTrue(match_prediction_true.is_a_exact_prediction())
        self.assertFalse(match_prediction_false.is_a_exact_prediction())
        self.assertFalse(match_prediction_2_false.is_a_exact_prediction())

        self.assertEqual(3, user.get_points())

    def test_get_user_points_from_one_moral_prediction(self):
        user = UserFactory()
        match = MatchFactory(finished = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = match.visitor_team_goals + 1,
                                           local_team_goals = match.local_team_goals + 1)

        self.assertTrue(match_prediction.is_a_moral_prediction())
        self.assertEqual(1, user.get_points())

    def test_get_user_points_from_some_moral_prediction_and_some_not(self):
        user = UserFactory()
        match = MatchFactory(finished = True, visitor_team_goals = 2, local_team_goals = 0)
        match_2 = MatchFactory(finished = True, visitor_team_goals = 0, local_team_goals = 2)

        match_prediction_true = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = 3,
                                           local_team_goals = 0)

        match_prediction_false = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 2)

        match_prediction_2_false = \
                UserMatchPredictionFactory(match = match_2,
                                           user = user, 
                                           visitor_team_goals = 1,
                                           local_team_goals = 0)

        match_prediction_2_true = \
                UserMatchPredictionFactory(match = match_2,
                                           user = user, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 4)

        self.assertTrue(match_prediction_true.is_a_moral_prediction())
        self.assertFalse(match_prediction_false.is_a_moral_prediction())
        self.assertFalse(match_prediction_2_false.is_a_moral_prediction())
        self.assertTrue(match_prediction_2_true.is_a_moral_prediction())

        self.assertEqual(2, user.get_points())

    def test_get_user_points_from_moral_and_exact_predictions(self):
        user = UserFactory()
        match = MatchFactory(finished = True, visitor_team_goals = 2, local_team_goals = 0)
        match_2 = MatchFactory(finished = True, visitor_team_goals = 0, local_team_goals = 2)
        match_3 = MatchFactory(finished = True)

        match_exact_prediction_true = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = 2,
                                           local_team_goals = 0) # points = 3

        match_exact_prediction_false = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 2) # points = 0

        match_exact_prediction_false_moral_prediction_true = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = 4,
                                           local_team_goals = 3) # points = 1

        match_2_exact_prediction_false_moral_prediction_true = \
                UserMatchPredictionFactory(match = match_2,
                                           user = user, 
                                           visitor_team_goals = 0,
                                           local_team_goals = 4) # points = 1

        match_3_exact_prediction_true = \
                UserMatchPredictionFactory(match = match_3,
                                           user = user, 
                                           visitor_team_goals = match_3.visitor_team_goals,
                                           local_team_goals = match_3.local_team_goals) # points = 3

        self.assertEqual(8, user.get_points())

    def test_get_user_points_from_one_correct_exact_prediction_of_a_classic_match(self):
        user = UserFactory()
        match = MatchFactory(finished = True, is_classic = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        self.assertEqual(6, user.get_points())

    def test_get_user_points_from_one_correct_moral_prediction_of_a_classic_match(self):
        user = UserFactory()
        match = MatchFactory(finished = True, is_classic = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           user = user, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        self.assertEqual(2, user.get_points())

    def test_get_user_points_from_one_correct_exact_prediction_with_double(self):
        user = UserFactory()
        match = MatchFactory(finished = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           is_double = True,
                                           user = user, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        self.assertEqual(6, user.get_points())

    def test_get_user_points_from_one_correct_moral_prediction_with_double(self):
        user = UserFactory()
        match = MatchFactory(finished = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           is_double = True,
                                           user = user, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        self.assertEqual(2, user.get_points())

    def test_get_user_points_from_one_correct_exact_prediction_with_double_of_a_classic_match(self):
        user = UserFactory()
        match = MatchFactory(finished = True, is_classic = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           is_double = True,
                                           user = user, 
                                           visitor_team_goals = match.visitor_team_goals,
                                           local_team_goals = match.local_team_goals)

        self.assertTrue(match_prediction.is_a_exact_prediction())
        self.assertEqual(12, user.get_points())

    def test_get_user_points_from_one_correct_moral_prediction_with_double_of_a_classic_match(self):
        user = UserFactory()
        match = MatchFactory(finished = True, is_classic = True)
        match_prediction = \
                UserMatchPredictionFactory(match = match,
                                           is_double = True,
                                           user = user, 
                                           visitor_team_goals = (match.visitor_team_goals + 1),
                                           local_team_goals = (match.local_team_goals + 1))

        self.assertTrue(match_prediction.is_a_moral_prediction())
        self.assertEqual(4, user.get_points())


from django.test import TestCase
from datetime import datetime, timedelta
from tournament.models import Team, Fixture, Match, User
from tournament.tests.factories import TeamFactory, FixtureFactory, MatchFactory, UserFactory

class TournamentTest(TestCase):

    def test_set_current_fixture(self):
        # Fixtures
        fixture = FixtureFactory()

        # Matchs
        match = MatchFactory(fixture = fixture)

        self.assertEqual(len(fixture.match_set.all()), 1)

    def test_get_current_fixture(self):
        # Fixtures
        current_fixture = FixtureFactory()
        past_fixture = FixtureFactory(date = (datetime.now() - timedelta(weeks = 1)))

        self.assertEqual(Fixture.get_current().id, current_fixture.id)

    def test_user_set_fixtures_results(self):
        # Fixtures
        fixture = FixtureFactory()

        # Matchs
        match = MatchFactory(fixture = fixture)

        # User
        user = UserFactory()
        user.set_match_result(match, 0, 0)

        self.assertEqual(len(user.usermatchprediction_set.all()), 1)

    def test_get_fixture_finished_matchs(self):
        # Fixtures
        fixture = FixtureFactory()

        # Matchs
        match = MatchFactory(fixture = fixture)
        match = MatchFactory(fixture = fixture, finished = True)
        match = MatchFactory(fixture = fixture, finished = True)

        self.assertEqual(fixture.get_finished_matchs().count(), 2)

    def test_get_user_finished_matchs(self):
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

    def test_compare_user_predictions_with_finished_matchs(self):
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

        self.assertEqual(len(user.get_good_predictions()), 2)
        self.assertEqual(user.get_points(), 4)

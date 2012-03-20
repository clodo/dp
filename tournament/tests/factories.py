import factory
from tournament.models import Team, Fixture, Match, User, UserMatchPrediction
from datetime import datetime, timedelta
from random import randrange

class TeamFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Team {0}'.format(n))

class FixtureFactory(factory.Factory):
    date = datetime.now()

class MatchFactory(factory.Factory):
    local_team = factory.LazyAttribute(lambda a: TeamFactory())
    visitor_team = factory.LazyAttribute(lambda a: TeamFactory())
    fixture = factory.LazyAttribute(lambda a: FixtureFactory())
    finished = False
    local_team_goals = randrange(0, 5)
    visitor_team_goals = randrange(0, 5)

class UserFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Name {0}'.format(n))

class UserMatchPredictionFactory(factory.Factory):
    user = factory.LazyAttribute(lambda a: UserFactory())
    match = factory.LazyAttribute(lambda a: MatchFactory())
    local_team_goals = randrange(0, 5)
    visitor_team_goals = randrange(0, 5)



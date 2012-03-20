import factory
from tournament.models import Team, Fixture, Match, User
from datetime import datetime, timedelta

class TeamFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Team {0}'.format(n))

class FixtureFactory(factory.Factory):
    date = datetime.now()

class MatchFactory(factory.Factory):
    local_team = factory.LazyAttribute(lambda a: TeamFactory())
    visitor_team = factory.LazyAttribute(lambda a: TeamFactory())
    fixture = factory.LazyAttribute(lambda a: FixtureFactory())
    finished = False
    local_team_goals = 0
    visitor_team_goals = 0

class UserFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'Name {0}'.format(n))




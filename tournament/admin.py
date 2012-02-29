from django.contrib import admin
from dp_site.tournament.models import Match, Team, Fixture

class MatchAdmin(admin.ModelAdmin):
    pass

class TeamAdmin(admin.ModelAdmin):
    pass

class FixtureAdmin(admin.ModelAdmin):
    pass

admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)

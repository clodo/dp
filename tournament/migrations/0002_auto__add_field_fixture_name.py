# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Fixture.name'
        db.add_column('tournament_fixture', 'name', self.gf('django.db.models.fields.CharField')(default='2012-02-28', max_length=50), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Fixture.name'
        db.delete_column('tournament_fixture', 'name')


    models = {
        'tournament.fixture': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Fixture'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'2012-02-28'", 'max_length': '50'})
        },
        'tournament.match': {
            'Meta': {'object_name': 'Match'},
            'fixture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Fixture']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'local_team'", 'to': "orm['tournament.Team']"}),
            'visitor_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visitor_team'", 'to': "orm['tournament.Team']"})
        },
        'tournament.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tournament.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tournament.usermatchresult': {
            'Meta': {'object_name': 'UserMatchResult'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_goals': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Match']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.User']"}),
            'visitor_goals': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['tournament']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Match.date'
        db.add_column('tournament_match', 'date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 31)), keep_default=False)

        # Deleting field 'Fixture.date'
        db.delete_column('tournament_fixture', 'date')

        # Adding field 'Fixture.number'
        db.add_column('tournament_fixture', 'number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Match.date'
        db.delete_column('tournament_match', 'date')

        # Adding field 'Fixture.date'
        db.add_column('tournament_fixture', 'date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today()), keep_default=False)

        # Deleting field 'Fixture.number'
        db.delete_column('tournament_fixture', 'number')


    models = {
        'tournament.fixture': {
            'Meta': {'ordering': "['-number']", 'object_name': 'Fixture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'2012-03-31'", 'max_length': '50'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'tournament.match': {
            'Meta': {'object_name': 'Match'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 3, 31)'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fixture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Fixture']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_classic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'local_team'", 'to': "orm['tournament.Team']"}),
            'local_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'visitor_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visitor_team'", 'to': "orm['tournament.Team']"}),
            'visitor_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
        'tournament.usermatchprediction': {
            'Meta': {'object_name': 'UserMatchPrediction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_double': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Match']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.User']"}),
            'visitor_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['tournament']

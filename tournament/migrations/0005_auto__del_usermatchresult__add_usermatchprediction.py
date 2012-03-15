# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'UserMatchResult'
        db.delete_table('tournament_usermatchresult')

        # Adding model 'UserMatchPrediction'
        db.create_table('tournament_usermatchprediction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.User'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Match'])),
            ('local_goals', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('visitor_goals', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('tournament', ['UserMatchPrediction'])


    def backwards(self, orm):
        
        # Adding model 'UserMatchResult'
        db.create_table('tournament_usermatchresult', (
            ('visitor_goals', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('local_goals', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Match'])),
        ))
        db.send_create_signal('tournament', ['UserMatchResult'])

        # Deleting model 'UserMatchPrediction'
        db.delete_table('tournament_usermatchprediction')


    models = {
        'tournament.fixture': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Fixture'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'2012-03-14'", 'max_length': '50'})
        },
        'tournament.match': {
            'Meta': {'object_name': 'Match'},
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fixture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Fixture']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'local_goals': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Match']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.User']"}),
            'visitor_goals': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['tournament']

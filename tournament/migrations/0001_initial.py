# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('tournament_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('tournament', ['User'])

        # Adding model 'Team'
        db.create_table('tournament_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('tournament', ['Team'])

        # Adding model 'Fixture'
        db.create_table('tournament_fixture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('tournament', ['Fixture'])

        # Adding model 'Match'
        db.create_table('tournament_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('local_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='local_team', to=orm['tournament.Team'])),
            ('visitor_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='visitor_team', to=orm['tournament.Team'])),
            ('fixture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Fixture'])),
        ))
        db.send_create_signal('tournament', ['Match'])

        # Adding model 'UserMatchResult'
        db.create_table('tournament_usermatchresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.User'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Match'])),
            ('local_goals', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('visitor_goals', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('tournament', ['UserMatchResult'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('tournament_user')

        # Deleting model 'Team'
        db.delete_table('tournament_team')

        # Deleting model 'Fixture'
        db.delete_table('tournament_fixture')

        # Deleting model 'Match'
        db.delete_table('tournament_match')

        # Deleting model 'UserMatchResult'
        db.delete_table('tournament_usermatchresult')


    models = {
        'tournament.fixture': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Fixture'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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

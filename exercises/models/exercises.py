from django.db import models
from django.utils import timezone


class Exercises(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', models.DO_NOTHING, db_column='user_id')
    learning_language = models.ForeignKey('accounts.Languages', models.DO_NOTHING, db_column='learning_language_id')
    source = models.CharField(max_length=20)
    title = models.CharField(max_length=255, blank=True, null=True)
    generation_settings = models.JSONField(blank=True, null=True)
    ai_prompt = models.TextField(blank=True, null=True)
    advanced_options = models.JSONField(blank=True, null=True)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'exercises'
        db_table_comment = 'Stores exercises created by registered users, including manually created exercises and AI-generated exercises.'

from django.db import models
from django.utils import timezone


class ExerciseItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    exercise = models.ForeignKey('exercises.Exercises', models.DO_NOTHING, db_column='exercise_id')
    position = models.IntegerField()
    sentence_template = models.TextField()
    correct_answers = models.JSONField()
    submitted_answers = models.JSONField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'exercise_items'
        unique_together = (('exercise', 'position'),)
        db_table_comment = 'Stores the individual sentences or questions belonging to an exercise, including accepted answers, submitted answers, and optional AI-generated explanations for incorrect answers.'

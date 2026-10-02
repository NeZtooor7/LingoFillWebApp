from django.conf import settings
from django.db import models

from .languages import Languages


class UsersLearningLanguages(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id")
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, db_column="language_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "users_learning_languages"
        unique_together = ("user", "language")
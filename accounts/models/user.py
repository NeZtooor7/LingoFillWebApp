from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=254)
    nickname = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    preferred_interface_language_id = models.BigIntegerField()
    default_learning_language_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_activity_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "first_name", "last_name", "preferred_interface_language_id"]

    class Meta:
        managed = False
        db_table = "account_users"
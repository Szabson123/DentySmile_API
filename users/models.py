from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from django.utils.text import slugify
import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        extra_fields['is_active'] = True

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    def __str__(self):
        return self.username

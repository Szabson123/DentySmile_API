from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from django.utils.text import slugify

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
    REQUIRED_FIELDS = ['first_name', 'last_name']
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.pk:  
            base_username = f'{slugify(self.first_name)}_{slugify(self.last_name)}'
            counter = 1
            username = base_username
            while CustomUser.objects.filter(username=username).exists():
                counter += 1
                username = f'{base_username}{counter}'
            self.username = username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

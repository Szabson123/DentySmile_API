from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, uuid=None, password=None, **extra_fields):
        if uuid is None:
            uuid = uuid.uuid4()
        user = self.model(uuid=uuid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uuid=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(uuid=uuid or str(uuid.uuid4()), password=password, **extra_fields)

ROLE = [
    ('admin', 'Admin'),
    ('reception', 'Reception'),
    ('doctor', 'Doctor'),
    ('none', 'None')
]

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    superadmin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=30, choices=ROLE, default='none')
    objects = UserManager()

    USERNAME_FIELD = 'uuid'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.username or self.uuid}'

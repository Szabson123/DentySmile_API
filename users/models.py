from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Użytkownik musi posiadać adres e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


ROLE = [
    ('admin', 'Admin'),
    ('reception', 'Reception'),
    ('doctor', 'Doctor'),
    ('none', 'None')
]

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE, default='none')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


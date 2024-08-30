from django.db import models
from users.models import CustomUser


class Institution(models.Model):
    name = models.CharField(max_length=255)
    localization = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, null=True, blank=True, related_name='institution_owner')
    admin = models.ManyToManyField(CustomUser, related_name='admin_in_institution')
    users = models.ManyToManyField(CustomUser, related_name='users_in_institution')

    def __str__(self):
        return self.name
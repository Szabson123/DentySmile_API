from django.db import models
from users.models import CustomUser


class Institution(models.Model):
    name = models.CharField(max_length=255)
    localization = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, null=True, blank=True, related_name='institution_owner', on_delete=models.CASCADE)
    admin = models.ManyToManyField(CustomUser, related_name='admin_in_institution', blank=True, null=True)
    users = models.ManyToManyField(CustomUser, related_name='users_in_institution', blank=True, null=True)

    def __str__(self):
        return self.name
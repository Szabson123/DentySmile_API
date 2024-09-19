from django.db import models
from users.models import CustomUser
from django_tenants.models import TenantMixin

class Institution(TenantMixin):
    name = models.CharField(max_length=255)
    localization = models.CharField(max_length=255)
    owner = models.ForeignKey('users.CustomUser', null=True, blank=True, related_name='institution_owner', on_delete=models.CASCADE)
    admin = models.ManyToManyField('users.CustomUser', related_name='admin_in_institution', blank=True)
    users = models.ManyToManyField('users.CustomUser', related_name='users_in_institution', blank=True)

    auto_create_schema = True

    def __str__(self):
        return self.name
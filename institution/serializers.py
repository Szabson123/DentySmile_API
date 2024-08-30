from rest_framework import serializers

from .models import Institution
from users.models import CustomUser
from users.serializers import UserSerializer

class InstitutionSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    admin = UserSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Institution
        fields = ['name', 'localization', 'owner', 'admin', 'users'] 
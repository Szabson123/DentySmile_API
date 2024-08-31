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
        

class CreatingUserToInsitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'password', 'uuid', 'role']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.is_active = True  
        user.save()
        return user
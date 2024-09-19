from rest_framework import serializers
from .models import CustomUser
from institution.models import Institution

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'id', 'uuid', 'role', 'superadmin', 'role']
        

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role']

    def validate_email(self, value):
        institution = self.context['request'].tenant
        if CustomUser.objects.filter(email=value, institution=institution).exists():
            raise serializers.ValidationError("Użytkownik z tym adresem e-mail już istnieje w tej klinice.")
        return value
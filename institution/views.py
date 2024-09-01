from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import Institution
from .serializers import InstitutionSerializer, CreatingUserToInsitutionSerializer
from users.models import CustomUser
from custom_auth.permissions import IsAdminOrOwnerOfInstitution, IsSuperAdmin

from drf_spectacular.utils import extend_schema, extend_schema_view

class InstitutionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

@extend_schema_view(create=extend_schema(exclude=True))
class CreatingUserToInsitution(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOfInstitution]

    @extend_schema(request=CreatingUserToInsitutionSerializer, responses={201: CreatingUserToInsitutionSerializer})
    @action(detail=True, methods=['POST'], url_path='register', url_name='register')
    def register(self, request, pk=None):  
        institution = Institution.objects.get(pk=pk)
        serializer = CreatingUserToInsitutionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.institution = institution 
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
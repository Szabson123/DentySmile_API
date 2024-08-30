from django.shortcuts import render

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import *
from .serializers import *
from users.models import *

class AllInstitutionViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'is_superadmin') or not user.is_superadmin:
            return Response({'error': 'You are not a superadmin and cannot access this information'}, status=status.HTTP_403_FORBIDDEN)
        
        institution = Institution.objects.all()
        serializer = InstitutionSerializer(institution, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

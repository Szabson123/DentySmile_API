from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Institution
from .serializers import InstitutionSerializer
from users.models import CustomUser


class InstitutionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InstitutionSerializer

    def list(self, request):
        user = request.user
        if not user.superadmin:
            return Response({'error': 'You are not a superadmin and cannot access this information'}, status=status.HTTP_403_FORBIDDEN)

        institutions = Institution.objects.all()
        serializer = InstitutionSerializer(institutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        institution = get_object_or_404(Institution, pk=pk)
        serializer = InstitutionSerializer(institution)
        return Response(serializer.data, status=status.HTTP_200_OK)
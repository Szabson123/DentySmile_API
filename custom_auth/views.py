from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.models import CustomUser
from institution.models import Institution
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer
from .permissions import IsAdminOrOwnerOfInstitution

from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from django.contrib.auth import authenticate


class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'uuid': {
                        'type': 'string',
                        'description': 'UUID of the user',
                    },
                    'password': {
                        'type': 'string',
                        'description': 'User password',
                    },
                },
                'required': ['uuid', 'password'],
            }
        },
        responses={
            200: OpenApiExample(
                'Token obtained successfully',
                value={
                    'refresh': 'refresh_token',
                    'access': 'access_token',
                },
            ),
            400: OpenApiExample(
                'Invalid credentials',
                value={'detail': 'Invalid credentials'},
            ),
        }
    )
    def post(self, request):
        user_uuid = request.data.get('uuid')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(uuid=user_uuid)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=user_uuid, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: 'Password change successfully',
            400: 'Bad request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Password changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(create=extend_schema(exclude=True))
class RegistrationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOfInstitution]

    @extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
    @action(detail=True, methods=['POST'], url_path='register', url_name='register')
    def register(self, request, pk=None):  
        institution = Institution.objects.get(pk=pk)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.institution = institution 
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'refresh': {
                        'type': 'string',
                        'description': 'Refresh token',
                    },
                },
                'required': ['refresh'],
            }
        },
        responses={
            205: OpenApiResponse(
                description="Token successfully blacklisted",
                examples=[OpenApiExample(
                    'Success',
                    value={"detail": "Token blacklisted successfully"}
                )]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[OpenApiExample(
                    'Bad Request',
                    value={"detail": "Invalid refresh token"}
                )]
            ),
        }
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    pass

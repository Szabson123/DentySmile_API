from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.models import CustomUser
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer

from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.contrib.auth import authenticate


class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'first_name': {
                        'type': 'string',
                        'description': 'First name of the user',
                    },
                    'last_name': {
                        'type': 'string',
                        'description': 'Last name of the user',
                    },
                    'password': {
                        'type': 'string',
                        'description': 'User password',
                    },
                },
                'required': ['first_name', 'last_name', 'password'],
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
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(first_name=first_name, last_name=last_name)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=user.username, password=password)

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
    @extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'user with this email already exist'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse

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

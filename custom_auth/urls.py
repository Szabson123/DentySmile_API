from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomLoginView, CustomTokenObtainPairView, LogoutView, CustomTokenRefreshView, ChangePasswordView


router = DefaultRouter()

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
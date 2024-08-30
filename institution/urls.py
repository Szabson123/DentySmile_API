from django.urls import path, include
from .views import InstitutionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'institution', InstitutionViewSet, basename='institutions')

urlpatterns = [
    path('', include(router.urls)),
]

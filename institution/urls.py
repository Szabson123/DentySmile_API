from django.urls import path, include
from .views import InstitutionViewSet, CreatingUserToInsitution
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', InstitutionViewSet, basename='institutions')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/create_user/', CreatingUserToInsitution.as_view({'post': 'register'}), name='create_user'),

]

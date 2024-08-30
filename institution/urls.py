from django.urls import path
from .views import AllInstitutionViewSet

urlpatterns = [
    path('all_institutions/', AllInstitutionViewSet.as_view(), name='all_institutions'),
]

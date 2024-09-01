from rest_framework import permissions
from institution.models import Institution


class IsAdminOrOwnerOfInstitution(permissions.BasePermission):
    def has_permission(self, request, view):
        institution_id = view.kwargs.get('pk')
        if not institution_id:
            return False
        try:
            institution = Institution.objects.get(pk=institution_id)
        except Institution.DoesNotExist:
            return False
        
        return request.user in institution.admin.all() or request.user == institution.owner
    

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.superadmin
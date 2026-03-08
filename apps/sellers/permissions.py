from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'seller')
        )
    

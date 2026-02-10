from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsProductSellerOrReadOnly(BasePermission):
    """
    Reading allowed.
    Written only for the seller who owns the product.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not hasattr(request.user, 'seller'):
            return False

        return obj.seller.user.id == request.user.id


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'seller')
        )
    


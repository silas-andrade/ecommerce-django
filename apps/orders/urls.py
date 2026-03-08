from rest_framework.routers import SimpleRouter

from django.urls import path

from .api.views.cart import (
    CartItemViewSet, 
    CartView,
    CartMergeSessionAPIView
)

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("cart/merge-session", CartMergeSessionAPIView.as_view(), name="cart-merge-session"),
]

router = SimpleRouter()
router.register(r"cart/items", CartItemViewSet, basename="cart-items")


urlpatterns += router.urls
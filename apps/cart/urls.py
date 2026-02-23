from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from django.urls import path

from .views import (
    CartItemViewSet, 
    CartView
)

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart-detail"),
]

router = SimpleRouter()
router.register(r"cart/items", CartItemViewSet, basename="cart-items")


urlpatterns += router.urls
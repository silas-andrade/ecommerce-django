from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import (
    ProductViewSet, 
    ProductMediaViewSet
)

router = SimpleRouter()
router.register(
    r'products',
    ProductViewSet,
    basename='products'
)

media_router = NestedSimpleRouter(
    router,
    r'products',
    lookup='product'
)

media_router.register(
    r'media',
    ProductMediaViewSet,
    basename='product-media'
)

urlpatterns = router.urls + media_router.urls

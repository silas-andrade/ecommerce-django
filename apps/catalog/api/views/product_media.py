from django.shortcuts import get_object_or_404
from django.db.models import Q


from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet 


from apps.catalog.api.serializers.product_media import (
    CreateProductMediaSerializer,
    UpdateProductMediaSerializer,
    ReadProductMediaSerializer,
)

from apps.catalog.api.permissions import IsProductSellerOrReadOnly
from apps.catalog.services.product import remove_product_media
from apps.catalog.models import ProductMedia, Product
from apps.catalog.choices import ProductStatus


class ProductMediaViewSet(ModelViewSet):
    serializer_class = ReadProductMediaSerializer

    serializer_action_classes = {
        'list': ReadProductMediaSerializer,
        'retrieve': ReadProductMediaSerializer,
        'create': CreateProductMediaSerializer,
        'update': UpdateProductMediaSerializer,
        'partial_update': UpdateProductMediaSerializer,
    }

    def get_queryset(self):
        qs = (
            ProductMedia.objects
            .filter(product_id=self.kwargs['product_pk'])
            .select_related('product', 'product__seller', 'product__seller__user')
        )

        if not self.request.user.is_authenticated:
            return qs.filter(product__status=ProductStatus.PUBLISHED)

        return qs.filter(
            Q(product__status=ProductStatus.PUBLISHED) |
            Q(product__seller__user=self.request.user)
        )

    def get_serializer_class(self):
        return self.serializer_action_classes.get(
            self.action,
            self.serializer_class
        )

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        return [
            IsAuthenticated(),
            IsProductSellerOrReadOnly(),
        ]

    def perform_create(self, serializer):
        product = get_object_or_404(
            Product,
            id=self.kwargs['product_pk'],
            seller__user=self.request.user
        )
        serializer.save(product=product)


    def perform_destroy(self, instance):
        remove_product_media(instance)
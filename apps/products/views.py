from django.shortcuts import get_object_or_404


from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed


from .serializers import (
    # Product
    CreateProductSerializer,
    ReadProductSerializer,
    UpdateProductSerializer,

    # ProductMedia
    CreateProductMediaSerializer,
    ReadProductMediaSerializer,
    UpdateProductMediaSerializer,
)
from .models import Product, ProductMedia
from .permissions import IsProductSellerOrReadOnly, IsSeller
from .choices import ProductStatus
from .exceptions import DomainError
from .services import publish_product, archive_product, remove_product_media


class ProductViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .select_related('seller', 'seller__user')
        .prefetch_related('media')
    )

    serializer_class = ReadProductSerializer

    serializer_action_classes = {
        'list': ReadProductSerializer,
        'retrieve': ReadProductSerializer,
        'create': CreateProductSerializer,
        'update': UpdateProductSerializer,
        'partial_update': UpdateProductSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes.get(
            self.action,
            self.serializer_class
        )

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        if self.action == 'create':
            return [
                IsAuthenticated(),
                IsSeller(),
            ]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [
                IsAuthenticated(),
                IsProductSellerOrReadOnly(),
            ]

        return super().get_permissions()


    @action(detail=True, methods=["post"], url_path="publish")
    def publish(self, request, pk=None):
        product = self.get_object()

        try:
            publish_product(product=product)
        except DomainError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductReadSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=["post"], url_path="archive")
    def archive(self, request, pk=None):
        product = self.get_object()

        try:
            archive_product(product=product)
        except DomainError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductReadSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        product = serializer.save(
            seller=self.request.user.seller
        )
        publish_product(product=product)

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")


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
        return (
            ProductMedia.objects
            .filter(product_id=self.kwargs['product_pk'])
            .select_related('product', 'product__seller', 'product__seller__user')
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
            id=self.kwargs['product_pk']
        )
        serializer.save(product=product)

    def perform_destroy(self, instance):
        remove_product_media(instance)
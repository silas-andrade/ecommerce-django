from django.db import models

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from apps.catalog.api.serializers.product import (
    UpdateProductSerializer,
    CreateProductSerializer,
    ReadProductSerializer,
)

from apps.catalog.api.permissions.product import IsProductSellerOrReadOnly

from apps.sellers.permissions import IsSeller
from apps.catalog.models import Product
from apps.catalog.exceptions import DomainError
from apps.catalog.choices import ProductStatus
from apps.catalog.services.product import (
    publish_product, 
    archive_product, 
)



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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = ReadProductSerializer(serializer.instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        qs = (
            Product.objects
            .select_related('seller', 'seller__user')
            .prefetch_related('media')
        )

        if not self.request.user.is_authenticated:
            return qs.filter(status=ProductStatus.PUBLISHED)

        return qs.filter(
            models.Q(status=ProductStatus.PUBLISHED) |
            models.Q(seller__user=self.request.user)
        )


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
        
        if self.action in ['publish', 'archive']:
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

        serializer = ReadProductSerializer(product)
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

        serializer = ReadProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(
            seller=self.request.user.seller
        )

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")




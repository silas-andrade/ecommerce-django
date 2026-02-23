from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet 
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.db import models

from .models import (
    Cart, 
    CartItem
    )

from .serializers import (
    # CartItem
    ReadCartItemSerializer,
    CreateCartItemSerializer,
    UpdateCartItemSerializer,

    # Cart
    ReadCartSerializer
)
from .services import (
    add_item_to_cart, 
    calculate_cart_total, 
    get_or_create_cart
    )
from .permissions import IsOwnerCart


class CartItemViewSet(ModelViewSet):
    queryset = (
        CartItem.objects.select_related('cart', 'cart__user', 'product')
    )

    serializer_class = ReadCartItemSerializer

    serializer_action_classes = {
        'list': ReadCartItemSerializer,
        'retrieve': ReadCartItemSerializer,
        'create': CreateCartItemSerializer,
        'update': UpdateCartItemSerializer,
        'partial_update': UpdateCartItemSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_or_create_cart(request)

        item = add_item_to_cart(
            product=serializer.validated_data["product"],
            cart=cart,
            quantity=serializer.validated_data["quantity"]
        )

        read_serializer = ReadCartItemSerializer(item)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        qs = CartItem.objects.select_related("product", "cart")

        if not self.request.session.session_key:
            self.request.session.create()

        if self.request.user.is_authenticated:
            return qs.filter(cart__user=self.request.user)

        return qs.filter(cart__session_key=self.request.session.session_key)


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
                IsOwnerCart(),
            ]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [
                IsOwnerCart(),
            ]
        
        return super().get_permissions()
    


class CartView(APIView):

    def get(self, request):
        cart = get_or_create_cart(request)
        serializer = ReadCartSerializer(cart)
        return Response(serializer.data)
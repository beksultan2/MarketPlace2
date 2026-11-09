from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer

CRUD_METHODS = ["get", "post", "put", "delete", "head", "options"]


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = CRUD_METHODS
    lookup_url_kwarg = "cart_id"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user.id).prefetch_related("items").order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)


@extend_schema(tags=["Cart Item"])
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = CRUD_METHODS
    lookup_url_kwarg = "item_id"
    filterset_fields = ["cart"]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user.id).order_by("id")

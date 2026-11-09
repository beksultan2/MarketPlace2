from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .filters import ProductFilter
from .models import Category, Product, ProductImage
from .permissions import IsOwnerOrReadOnly
from .serializers import CategorySerializer, ProductImageSerializer, ProductSerializer


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    search_fields = ["category_name"]
    ordering_fields = ["id", "category_name"]


@extend_schema(tags=["Product"])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related("images").order_by("-created_date")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_class = ProductFilter
    search_fields = ["product_name", "description", "article_number"]
    ordering_fields = ["price", "created_date", "product_name"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.id)


@extend_schema(tags=["Product Image"])
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.select_related("product").order_by("id")
    serializer_class = ProductImageSerializer
    filterset_fields = ["product"]

    def _check_owner(self, product):
        if product.owner != self.request.user.id:
            raise PermissionDenied("Бул product сизге таандык эмес")

    def perform_create(self, serializer):
        self._check_owner(serializer.validated_data["product"])
        serializer.save()

    def perform_update(self, serializer):
        self._check_owner(serializer.instance.product)
        serializer.save()

    def perform_destroy(self, instance):
        self._check_owner(instance.product)
        instance.delete()

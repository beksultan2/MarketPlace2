from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductImageViewSet, ProductViewSet

router = DefaultRouter()
router.include_root_view = False
router.register("category", CategoryViewSet, basename="category")
router.register("product", ProductViewSet, basename="product")
router.register("product-image", ProductImageViewSet, basename="product-image")

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from .views import CartItemViewSet, CartViewSet

router = DefaultRouter()
router.include_root_view = False
router.register("cart", CartViewSet, basename="cart")
router.register("cart-item", CartItemViewSet, basename="cart-item")

urlpatterns = router.urls

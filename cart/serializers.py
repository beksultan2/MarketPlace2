from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity")

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("quantity кеминде 1 болушу керек")
        return value

    def validate_cart(self, cart):
        request = self.context.get("request")
        if request and cart.user != request.user.id:
            raise serializers.ValidationError("Бул cart сизге таандык эмес")
        return cart


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "items")
        read_only_fields = ("id", "user")

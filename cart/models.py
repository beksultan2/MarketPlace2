from django.db import models


class Cart(models.Model):
    user = models.IntegerField()

    def __str__(self):
        return f"Cart #{self.pk} (user {self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cart_id}: product {self.product} x{self.quantity}"

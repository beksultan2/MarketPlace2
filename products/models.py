from django.db import models


class Category(models.Model):
    category_image = models.ImageField(upload_to="categories/", null=True, blank=True)
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    article_number = models.CharField(max_length=100, unique=True)
    is_official = models.BooleanField(default=False)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.IntegerField()

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    product_image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.product.product_name} #{self.pk}"

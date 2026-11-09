import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    created_after = django_filters.DateTimeFilter(field_name="created_date", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["category", "is_official", "owner", "price_min", "price_max",
                  "created_after", "created_before"]

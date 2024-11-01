from rest_framework.pagination import PageNumberPagination
import django_filters
from .models import *


class PurchaseFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='purchased_date', lookup_expr='year')
    purchased_date_range = django_filters.DateTimeFromToRangeFilter(field_name='purchased_date')
    class Meta:
        model = Purchase
        fields = [ "total", "active", "employee", "year", "purchased_date_range"]

class PurchasePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
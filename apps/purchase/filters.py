from rest_framework.pagination import PageNumberPagination
import django_filters
from .models import *


class PurchaseFilter(django_filters.FilterSet):

    class Meta:
        model = Purchase
        fields = [ "total", "active", "employee", ]

class PurchasePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
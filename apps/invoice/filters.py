from rest_framework.pagination import PageNumberPagination
import django_filters
from .models import *


class InvoiceFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='read_date', lookup_expr='year')

    class Meta:
        model = Invoice
        fields = [ "employee", "usuario", "status", "year", ]

class InvoicePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
import django_filters
from rest_framework.pagination import PageNumberPagination
from .models import InvoiceHistory

class InvoiceHistoryFilter(django_filters.FilterSet):
    class Meta:
        model = InvoiceHistory
        fields = [ "id", "invoice"]

class GenericPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    # page_size = 20
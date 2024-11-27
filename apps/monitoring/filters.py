from rest_framework.pagination import PageNumberPagination
import django_filters
from .models import *


class MonitoringFilter(django_filters.FilterSet):
    read_date_range = django_filters.DateTimeFromToRangeFilter(field_name='read_date')
    year = django_filters.NumberFilter(field_name='read_date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='read_date', lookup_expr='month')
    class Meta:
        model = Monitoring
        fields = [ "created", "read_date", "measured", "status",]

class MonitoringPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 10
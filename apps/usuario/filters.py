import django_filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import *


class UsuarioFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="search_filter")

    class Meta:
        model = Usuario
        fields = [ "ci", "names", "lastnames", "family", "status", ]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(names__icontains=value) | 
            Q(lastnames__icontains=value) |
            Q(family__icontains=value) |
            Q(ci__icontains=value)
        )
        

class UsuarioPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
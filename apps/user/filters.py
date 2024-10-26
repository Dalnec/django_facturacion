from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import django_filters
from .models import *


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = [ "username", "profile" ]

class UserPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20



    
class EmployeeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="search_filter")

    class Meta:
        model = Employee
        fields = [ "ci", "names", "lastnames", "status", ]
    
    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(names__icontains=value) | 
            Q(lastnames__icontains=value) |
            Q(ci__icontains=value)
        )

class EmployeePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
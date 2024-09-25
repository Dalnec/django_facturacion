from rest_framework.pagination import PageNumberPagination
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

    class Meta:
        model = Employee
        fields = [ "ci", "names", "lastnames", "status", ]

class EmployeePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
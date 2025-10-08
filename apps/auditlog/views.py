from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend

from .filters import InvoiceHistoryFilter, GenericPagination
from .serializers import InvoiceHistorySerializer
from .models import InvoiceHistory

    
class InvoiceHistoryView(viewsets.GenericViewSet):
    serializer_class = InvoiceHistorySerializer
    queryset = InvoiceHistory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = InvoiceHistoryFilter
    pagination_class = GenericPagination
    ordering_fields = ['id', 'read_date']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
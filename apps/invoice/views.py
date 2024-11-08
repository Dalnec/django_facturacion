from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.purchase.models import Purchase

from .models import *
from .serializers import *
from .filters import *

class InvoiceView(viewsets.GenericViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = InvoiceFilter
    pagination_class = InvoicePagination
    ordering_fields = ['id', 'read_date']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        purchase = Purchase.objects.all().order_by('id').last()
        last_measured = Invoice.objects.filter(usuario=data['usuario']).order_by('id').last()
        measured = float(data['measured']) - float(last_measured.measured)
        # TODO: Calcular el total y validar el valor limite del medidor
        if (measured <= 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data['price'] = purchase.price
        data['total'] = f"{round(measured * float(purchase.price), 2)}"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        instance = self.get_object()
        instance.status = request.data.get('status', None)
        instance.save()
        return Response(status=status.HTTP_200_OK)
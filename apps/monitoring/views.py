from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.renderers import TemplateHTMLRenderer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, ExpressionWrapper, FloatField
from drf_spectacular.utils import extend_schema

import io
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from .models import *
from .serializers import *
from .filters import *

@extend_schema(tags=["Monitoring"])
class MonitoringView(viewsets.GenericViewSet):
    serializer_class = MonitoringSerializer
    queryset = Monitoring.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MonitoringFilter
    pagination_class = MonitoringPagination
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
        # print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        monitor = serializer.save()
        monitor.measured = round(monitor.measured, 2)
        monitor.save()
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], serializer_class=LastMonitoringSerializer)
    def get_last(self, request):
        queryset = self.get_queryset().order_by('pk').last()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def get_monitorings(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], renderer_classes=[TemplateHTMLRenderer])
    def report(self, request, *args, **kwargs):
        params = request.query_params.dict()
        queryset = self.filter_queryset(self.get_queryset().order_by('-id'))
        # annotae altura - medido
        # queryset = queryset.annotate(altura=ExpressionWrapper(F('height') - F('measured'), output_field=FloatField()))
        monitorings = []
        for monitoring in queryset:
            monitoring.altura = round(float(monitoring.height) - float(monitoring.measured), 2)
            monitorings.append(monitoring)
        # queryset = monitorings
        data = {
            "monitorings": monitorings,
            "counter": 0,
            "period": self.period(params['month'], params['year']),
            "params": params,
        }
        # return Response(data, template_name='./monitorings.html', status=status.HTTP_200_OK)
       
        html = render_to_string('monitorings.html', data)
        pdf_file = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=pdf_file)
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Reporte_Monitoreo.pdf"'
        return response
    
    def period(self, month, year):
        if month == '1':
            month = 'Enero'
        elif month == '2':
            month = 'Febrero'
        elif month == '3':
            month = 'Marzo'
        elif month == '4':
            month = 'Abril'
        elif month == '5':
            month = 'Mayo'
        elif month == '6':
            month = 'Junio'
        elif month == '7':
            month = 'Julio'
        elif month == '8':
            month = 'Agosto'
        elif month == '9':
            month = 'Septiembre'
        elif month == '10':
            month = 'Octubre'
        elif month == '11':
            month = 'Noviembre'
        elif month == '12':
            month = 'Diciembre'
        return f"{month} {year}"
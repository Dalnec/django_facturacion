from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import TemplateHTMLRenderer
from apps.purchase.models import Purchase

from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

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
        data = request.data.copy()
        measured = float(data['measured']) - float(data['previosMeasured'])
        if (measured <= 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
    

    @action(detail=True, methods=['GET'], renderer_classes=[TemplateHTMLRenderer])
    def ticket(self, request, pk=None, format=None, *args, **kwargs):
        invoice = self.get_object()
        data = self.serializer_class(invoice).data
        ticket = json.loads(data['ticket'])
        data = {
            'header': ticket['header'],
            'body': ticket['body'],
        }
        return Response(data, template_name='./ticket.html', status=status.HTTP_200_OK)


class InvoiceTicketView(RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, uuid=None, *args, **kwargs):
        import io
        from django.template.loader import render_to_string
        from datetime import datetime

        invoice = self.get_object()
        data = self.serializer_class(invoice).data
        ticket = json.loads(data['ticket'])
        data = {
            'header': ticket['header'],
            'body': ticket['body'],
        }

        # Renderiza la plantilla HTML con los datos de la factura
        html = render_to_string('ticket.html', data)

        # Crea un objeto de bytes
        pdf_file = io.BytesIO()
        # Define el tamaño de la página en puntos (1 mm ≈ 2.83465 puntos)
        # 80 mm de ancho ≈ 227 puntos y un alto que puedes ajustar según el contenido.
        page_width = 227  # 80 mm en puntos
        page_height = 300

        # CSS para ajustar el tamaño de la página en el PDF
        custom_css = f"""
        @page {{
            size: {page_width}pt {page_height}pt;
            margin: 5;
        }}
        body {{
            width: {page_width}pt;
            font-size: 15px;
            margin: 0;
            padding: 10px;
            font-family: Arial, sans-serif;
        }}
        """

        # Combina el CSS personalizado con el HTML
        full_html = f"<style>{custom_css}</style>{html}"

        # Convierte el HTML a PDF usando xhtml2pdf
        pisa.CreatePDF(io.BytesIO(full_html.encode("UTF-8")), dest=pdf_file)

        # Prepara la respuesta HTTP con el PDF
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Recibo_{ticket['body']['actual_month']}_{ticket['header']['full_name']}.pdf"'
        return response
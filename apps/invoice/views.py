import json
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.renderers import TemplateHTMLRenderer
from apps.auditlog.serializers import InvoiceHistorySerializer
from apps.purchase.models import Purchase

from django.http import HttpResponse
from django.db import transaction
from django.db.models import Sum
# from io import BytesIO
import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from apps.usuario.models import Usuario, UsuarioDetail
from apps.distric.models import Distric
from datetime import date, datetime
from decimal import Decimal
from .models import Invoice  
from .serializers import InvoiceSerializer  
from .filters import InvoiceFilter, InvoicePagination
from apps.auditlog.models import InvoiceHistory

from dateutil.relativedelta import relativedelta

@extend_schema(tags=["Invoice"])
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
        with transaction.atomic():
            data = request.data.copy()
            purchase = Purchase.objects.all().order_by('id').last()
            invoices = Invoice.objects.filter(usuario=data['usuario']).order_by('id')
            usuario = Usuario.objects.get(id=data['usuario'])
            distric = Distric.objects.get(id=1)
            measured = 0
            last_measured = 0

            if not invoices.exists():
                if usuario.last_measured != 0 and not usuario.last_measured:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                last_measured = usuario.last_measured
            else:
                last_measured = invoices.last().measured
                # Generacion de multa
                # if last_measured.status == 'D':
                #     UsuarioDetail.generate_mora(usuario)

            if usuario.restart:
                measured = float(data['measured'])
                usuario.restart = False
                usuario.save()
            else:
                measured = float(data['measured']) - float(last_measured)
            if (measured < 0):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            data['price'] = purchase.price
            if (measured > 0 and measured < 1):
                data['subtotal'] = purchase.price
            else:
                data['subtotal'] = f"{Invoice.custom_round(measured * float(purchase.price))}"
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            invoice = serializer.save()

            today = datetime.today()
            last_month = today - relativedelta(months=1)
            invoice.billing_month = last_month.replace(day=1).date()

            # Generacion de multa
            if distric.settings["auto_penalty"]:
                depts = Invoice.objects.filter(usuario=data['usuario'], status='D').exclude(id=invoice.id)
                if depts.exists():
                    UsuarioDetail.generate_mora(usuario, distric.settings["penalty_amount"], invoice)

            # INFO: Actualiza el 'detalle del usuario' donde estado debe ser true para agregar al detalle del recibo
            detail = invoice.usuario.fk_usuariodetail_usuario.filter(invoice__isnull=True, status=True)
            # INFO: Actualiza total de invoice en caso tenga detalle
            if detail.exists():
                income = detail.filter(is_income=True).aggregate(total=Sum('subtotal'))['total'] or 0
                outcome = detail.filter(is_income=False).aggregate(total=Sum('subtotal'))['total'] or 0
                invoice.total = Invoice.custom_round(invoice.subtotal + income - outcome)
                detail.update(invoice=invoice.id)
            else:
                invoice.total = invoice.subtotal
            invoice.save()
            
            detail_penalty = invoice.usuario.fk_usuariodetail_usuario.filter(invoice__id=invoice.id, status=True)
            if detail_penalty.exists():
                income = detail_penalty.filter(is_income=True).aggregate(total=Sum('subtotal'))['total'] or 0
                outcome = detail_penalty.filter(is_income=False).aggregate(total=Sum('subtotal'))['total'] or 0
                invoice.total = Invoice.custom_round(invoice.subtotal + income - outcome)
                invoice.save()
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            purchase = Purchase.objects.all().order_by('id').last()
            partial = kwargs.pop('partial', False)
            data = request.data.copy()
            instance = self.get_object()
            before = Invoice.objects.get(pk=instance.pk)

            usuario = instance.usuario
            if usuario.restart:
                measured = Decimal(data['measured'])
                usuario.restart = False
                usuario.save()
            else:
                measured = Decimal(data['measured']) - Decimal(data['previosMeasured'])
            if (measured < 0):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            today = date.today()
            if today == instance.read_date.date():
                instance.price = purchase.price
            instance.subtotal = Invoice.custom_round(measured * instance.price)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            invoice = serializer.save()
            
            detail = invoice.usuario.fk_usuariodetail_usuario.filter(invoice=invoice.id, status=True)
            if detail.exists():
                income = detail.filter(is_income=True).aggregate(total=Sum('subtotal'))['total'] or 0
                outcome = detail.filter(is_income=False).aggregate(total=Sum('subtotal'))['total'] or 0
                invoice.total = Invoice.custom_round(invoice.subtotal + income - outcome)
            else:
                invoice.total = invoice.subtotal
            invoice.save()

            # validacion de totales en caso existan invoices mayores
            invoices = Invoice.objects.filter(usuario__id=usuario.id, id__gt=invoice.id).order_by('id')
            if invoices.exists():
                for i in invoices:
                    i.subtotal = Invoice.custom_round(i.measured_diff * i.price)
                    v_detail = i.usuario.fk_usuariodetail_usuario.filter(invoice=i.id, status=True)
                    if v_detail.exists():
                        income = v_detail.filter(is_income=True).aggregate(total=Sum('subtotal'))['total'] or 0
                        outcome = v_detail.filter(is_income=False).aggregate(total=Sum('subtotal'))['total'] or 0
                        i.total = Invoice.custom_round(i.subtotal + income - outcome)
                    else:
                        i.total = i.subtotal
                    i.save()
            
            InvoiceHistory.objects.create(
                invoice=invoice,
                employee=request.user.fk_employee_user if request.user.is_authenticated else None,
                changes=InvoiceHistory.get_diff(before, invoice),
                action='update'
            )

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
        # Construcción del contexto
        context = {
            'header': ticket['header'],
            'body': ticket['body'],
            'details': ticket['details'],
        }

        return Response(context, template_name='./ticket.html', status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], renderer_classes=[TemplateHTMLRenderer])
    def status_report(self, request, *args, **kwargs):
        # params = request.GET.dict()
        params = request.query_params.dict()
        queryset = self.filter_queryset(self.get_queryset().order_by('-id'))
        # concatenar en observaciones los detalles de la factura
        invoices = []
        for invoice in queryset:
            details = invoice.fk_usuariodetail_invoice.all()
            if details.exists():
                for detail in details:
                    if invoice.observations and invoice.observations != '' and invoice.observations != 'None':
                        invoice.observations = f"{invoice.observations} | {detail.description} {detail.subtotal}"
                    else:
                        invoice.observations = f"{detail.description} {detail.subtotal}"
            else:
                invoice.observations = '' if invoice.observations is None else invoice.observations
            invoices.append(invoice)
        # queryset = queryset.annotate(
        #     details=Concat(
        #         Case(
        #             When(observations__isnull=True, then=Value('')),  # Si es None, usa una cadena vacía
        #             default=F('observations'),  # Usa el valor de observations si no es None
        #             output_field=TextField()
        #         ),
        #         Value(' | '),  # Separador
        #         Subquery(
        #             UsuarioDetail.objects.filter(invoice=OuterRef('id'))
        #             .values('invoice')
        #             .annotate(
        #                 detalles_concat=StringAgg('description', delimiter=' | ')
        #             )
        #             .values('detalles_concat')
        #         ),
        #         output_field=TextField()
        #     )
        # )
        data = {
            "invoices": invoices,
            "counter": 0,
            "period": self.period(params['month'], params['year']),
            "params": params,
            "total": queryset.aggregate(total=Sum('total'))['total'] or 0.0,
            "count_depts": queryset.filter(status='D').count(),
            "count_paid": queryset.filter(status='P').count(),
        }
        # return Response(data, template_name='./invoices.html', status=status.HTTP_200_OK)
       
        html = render_to_string('invoices.html', data)
        pdf_file = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=pdf_file)
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte_de_facturas.pdf"'
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


    @action(detail=False, methods=['GET'], renderer_classes=[TemplateHTMLRenderer])
    def report_usuario(self, request, *args, **kwargs):
        params = request.query_params.dict()
        queryset = self.filter_queryset(self.get_queryset().order_by('-id'))
        
        invoices = []
        for invoice in queryset:
            details = invoice.fk_usuariodetail_invoice.all()
            if details.exists():
                for detail in details:
                    if invoice.observations and invoice.observations != '' and invoice.observations != 'None':
                        invoice.observations = f"{invoice.observations} | {detail.description} {detail.subtotal}"
                    else:
                        invoice.observations = f"{detail.description} {detail.subtotal}"
            else:
                invoice.observations = '' if invoice.observations is None else invoice.observations
            invoices.append(invoice)

        data = {
            "invoices": invoices,
            "usuario": queryset.first().usuario,
            "counter": 0,
            "period": params['year'],
            "params": params,
            "total": queryset.aggregate(total=Sum('total'))['total'] or 0.0,
            "count_depts": queryset.filter(status='D').count(),
            "count_paid": queryset.filter(status='P').count(),
        }
        html = render_to_string('invoices_usuario.html', data)
        pdf_file = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=pdf_file)
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte_de_facturas.pdf"'
        return response
    
    @action(detail=True, methods=['GET'], serializer_class=InvoiceHistorySerializer, filterset_class=None)
    def history(self, request, pk=None):
        instance = self.get_object()
        history = InvoiceHistory.objects.filter(invoice__id=instance.id).order_by('-created')
        serializer = self.get_serializer(history, many=True)
        # data = serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Invoice"])
class InvoiceTicketView(RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, uuid=None, *args, **kwargs):
        invoice = self.get_object()
        data = self.serializer_class(invoice).data
        ticket = json.loads(data['ticket'])
        data = {
            'header': ticket['header'],
            'body': ticket['body'],
            'details': ticket['details'],
        }

        # Renderiza la plantilla HTML con los datos de la factura
        html = render_to_string('ticket.html', data)

        # Crea un objeto de bytes
        pdf_file = io.BytesIO()
        # Define el tamaño de la página en puntos (1 mm ≈ 2.83465 puntos)
        # 80 mm de ancho ≈ 227 puntos y un alto que puedes ajustar según el contenido.
        page_width = 227  # 80 mm en puntos
        page_height = 330

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
        response['Content-Disposition'] = f'attachment; filename="Recibo_{ticket["body"]["actual_month"]}_{ticket["header"]["full_name"]}.pdf"'
        return response
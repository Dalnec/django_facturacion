import django_filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F
from django.db.models import (
    Case, 
    When, 
    Value,
    Exists, 
    OuterRef, 
    Subquery, 
    DateTimeField, 
    BooleanField
)
from django.db.models.functions import Now, ExtractMonth
import datetime
from .models import *
from apps.invoice.models import Invoice


class UsuarioFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="search_filter", label="Busqueda general")
    hasDebt = django_filters.BooleanFilter(method="hasDebt_filter", label="Tiene Deuda?")
    makeInvoice = django_filters.BooleanFilter(method="makeInvoice_filter", label="Factura disponible a realizar?")

    class Meta:
        model = Usuario
        fields = [ "ci", "names", "lastnames", "family", "status", "hasDebt", "makeInvoice"]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(ci__icontains=value) |
            Q(names__icontains=value) | 
            Q(lastnames__icontains=value) |
            Q(family__icontains=value) 
        )

    def hasDebt_filter(self, queryset, name, value):
        invoices_with_debt = Invoice.objects.filter(
            usuario=OuterRef('pk'),
            status='D'
        )
        
        return queryset.annotate(
            has_debt_annotation=Exists(invoices_with_debt)
        ).filter(has_debt_annotation=value)
    
    def makeInvoice_filter(self, queryset, name, value):
        # Subconsulta para obtener la fecha de la última lectura de factura
        last_invoice_subquery = Invoice.objects.filter(
            usuario=OuterRef('pk')
        ).order_by('-read_date').values('read_date')[:1]

        # Anotamos la fecha de la última factura en el queryset del usuario
        queryset = queryset.annotate(
            last_invoice_date=Subquery(last_invoice_subquery, output_field=DateTimeField())
        )

        # Obtenemos la fecha actual y los límites de 20 días atrás
        now = timezone.now()
        twenty_days_ago = now - datetime.timedelta(days=20)

        # Anotamos el mes de la última factura y el mes actual
        queryset = queryset.annotate(
            last_invoice_month=ExtractMonth('last_invoice_date'),
            current_month=ExtractMonth(Now())
        )

        # Anotamos si el usuario puede hacer una nueva factura
        queryset = queryset.annotate(
            can_make_invoice=Case(
                # Si no existe una factura previa, puede hacer una nueva factura
                When(last_invoice_date__isnull=True, then=Value(True)),
                # Si la última factura no fue creada en el mes actual y tiene más de 20 días
                When(
                    last_invoice_month__lt=F('current_month'),
                    last_invoice_date__lte=twenty_days_ago,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        
        # Filtramos según el valor booleano que se pase (True o False)
        return queryset.filter(can_make_invoice=value)
        

class UsuarioPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20




class UsuarioDetailFilter(django_filters.FilterSet):

    class Meta:
        model = UsuarioDetail
        fields = [ "usuario", "invoice",]


class UsuarioDetailPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
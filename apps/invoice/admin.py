from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Invoice

class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice

class InvoiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = InvoiceResource


admin.site.register(Invoice, InvoiceAdmin)
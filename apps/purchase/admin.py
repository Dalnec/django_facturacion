from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Purchase


class PurchaseResource(resources.ModelResource):
    class Meta:
        model = Purchase

class PurchaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PurchaseResource


admin.site.register(Purchase, PurchaseAdmin)
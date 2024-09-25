from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Monitoring


class MonitoringResource(resources.ModelResource):
    class Meta:
        model = Monitoring

class MonitoringAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MonitoringResource


admin.site.register(Monitoring, MonitoringAdmin)
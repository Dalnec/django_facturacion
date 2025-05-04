from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Usuario, UsuarioDetail

class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario

class UsuarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UsuarioResource

# class UsuarioDetailAdmin(admin.ModelAdmin):
#     list_filter = ("usuario",)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(UsuarioDetail)

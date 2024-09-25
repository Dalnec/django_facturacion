import os

# Ruta a la carpeta que contiene las apps
apps_dir = os.path.join(os.getcwd(), 'apps')

# Recorremos cada subcarpeta en la carpeta de apps
for app_name in os.listdir(apps_dir):
    app_path = os.path.join(apps_dir, app_name)
    
    # Verificamos que sea una carpeta
    if os.path.isdir(app_path) and not app_name.startswith('_') and not app_name == 'seeder':
        print(app_path)
        # Definimos la ruta del archivo routers.py dentro de la carpeta de la app
        routers_file_path = os.path.join(app_path, 'routers.py')
        
        # Si el archivo routers.py no existe, lo creamos
        if not os.path.exists(routers_file_path):
            with open(routers_file_path, 'w') as routers_file:
                # Puedes agregar cualquier contenido inicial que quieras al archivo routers.py
                routers_file.write("# Routers for app: {}\n".format(app_name))
                routers_file.write("from django.urls import include, path\n")
                routers_file.write("from rest_framework.routers import DefaultRouter\n")
                routers_file.write("from .views import *\n\n")
                routers_file.write("router = DefaultRouter()\n")
                routers_file.write("# Example: router.register(r'endpoint', views.ViewSet, basename='basename')\n")
                routers_file.write("# urlpatterns = router.urls\n")
                routers_file.write("# urlpatterns = [ path("", include(router.urls)), ]\n")
            print(f"Creado {routers_file_path}")
        else:
            print(f"{routers_file_path} ya existe")

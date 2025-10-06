import json
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.user.models import Profile
from apps.distric.models import Distric
from apps.user.serializers import UserSerializer, EmployeeSerializer
from apps.usuario.serializers import UsuarioSerializer

from .serializers import SeedingSerializer

class SeedingView(GenericViewSet):
    serializer_class = SeedingSerializer

    def create(self, request, *args, **kwargs):

        try:
            # User.objects.create_superuser('ADMIN', 'admin')
            Profile.objects.get_or_create( id=1, description="ADMINISTRADOR" )
            Profile.objects.get_or_create( id=2, description="LECTURADOR" )
            Profile.objects.get_or_create( id=3, description="USUARIO" )

            self.seed_employees()
            self.seed_usuarios()

            # file_resources = {
            #     'apps/seeder/data/monitoring.json': MonitoringResource(),
            #     'apps/seeder/data/invoices.json': InvoiceResource(),
            #     'apps/seeder/data/purchases.json': PurchaseResource(),
            # }


            # for file_path, resource_model in file_resources.items():
            #     dataset = Dataset()

            #     with open(file_path, 'r', encoding='utf-8') as json_file:
            #         json_data = json.load(json_file)
            #         dataset.dict = json_data

            #     result = resource_model.import_data(dataset, dry_run=False)

            #     if result.has_errors():
            #         errors = result.row_errors()
            
            Distric.objects.get_or_create(
                id=1,
                name="OTB BARRIO LUZ",
                address="CALLE DOS DE MAYO 799",
                representative="JIMMY",
                phone="65359585",
                email="otb@otb.com",
                settings={"width": "240", "height": "240", "length": "230", "force_ci": True, "auto_penalty": True, "penalty_amount": 50, "interval_time_device": 1200000, "collect_previous_month": False}
            )

            return Response('Seeding Completed!', status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def seed_employees(self, *args, **kwargs):
        employee_data = [
            {
                "ci": "7777777",
                "names": "administrador",
                "lastnames": "administrador",
                "email": "admin@admin.com",
                "phone": "78945612",
                "address": "Calle Beni 100",
                "status": "A",
                "username": "administrador",
                "password": "123456",
                "profile": 1
            },

            {
                "ci": "1013577",
                "names": "facturador",
                "lastnames": "facturador",
                "email": "factur@factur.com",
                "phone": "77967878",
                "address": "Calle Juan Pablo 101",
                "status": "A",
                "username": "1013577",
                "password": "1013577",
                "profile": 2
            }
        ]

        for employee in employee_data:
            user_serializer = UserSerializer(data=employee)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            serializer = EmployeeSerializer(data=employee)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

        
    def seed_usuarios(self, *args, **kwargs):
        
        with open('apps/seeder/data/usuarios.json', 'r') as json_file:
            usuarios_data = json.load(json_file)

        for usuario in usuarios_data:
            user_serializer = UserSerializer(data=usuario)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            serializer = UsuarioSerializer(data=usuario)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
import json
from apps.user.models import Profile, User
from apps.distric.models import Distric
from apps.user.serializers import UserSerializer, EmployeeSerializer
from apps.usuario.serializers import UsuarioSerializer
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'Datos Iniciales'
    def handle(self, *args, **kwargs):
        try:
            User.objects.create_superuser('ADMIN', 'admin')
            Profile.objects.get_or_create( id=1, description="ADMINISTRADOR" )
            Profile.objects.get_or_create( id=2, description="LECTURADOR" )
            Profile.objects.get_or_create( id=3, description="USUARIO" )

            self.seed_employees()
            self.seed_usuarios()

            Distric.objects.get_or_create(
                id=1,
                name="OTB BARRIO LUZS",
                address="CALLE DOS DE MAYO 799",
                representative="JIMMY",
                phone="65359585",
                email="otb@otb.com",
                settings={"width": "240", "height": "240", "length": "230", "interval_time_device": 1500000}
            )

            print("Datos Iniciales Creados")

        except Exception as e:
            print(e)
    
    def seed_employees(self, *args, **kwargs):
        employee_data = [
            {
                "ci": "7456321",
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
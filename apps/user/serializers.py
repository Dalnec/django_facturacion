from rest_framework import serializers

from apps.usuario.serializers import UsuarioSerializer
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

        
class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    profile = serializers.ReadOnlyField(source="user.profile.id")
    profile_description = serializers.ReadOnlyField(source="user.profile.description")
    class Meta:
        model = Employee
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UsuarioUserSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source="id")
    usuario_id = serializers.ReadOnlyField(source="fk_usuario_user.id")
    names = serializers.ReadOnlyField(source="fk_usuario_user.names")
    lastnames = serializers.ReadOnlyField(source="fk_usuario_user.lastnames")
    status = serializers.ReadOnlyField(source="fk_usuario_user.status")
    profile_id = serializers.ReadOnlyField(source="profile.id")
    profile_description = serializers.ReadOnlyField(source="profile.description")

    class Meta:
        model = User
        fields = (
            "user_id",
            "usuario_id",
            "username",
            "is_staff",
            "is_active",
            "is_owner",
            "names",
            "lastnames",
            "status",
            "profile_id",
            "profile_description",
        )


class EmployeeUserSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source="id")
    employee_id = serializers.ReadOnlyField(source="fk_employee_user.id")
    names = serializers.ReadOnlyField(source="fk_employee_user.names")
    lastnames = serializers.ReadOnlyField(source="fk_employee_user.lastnames")
    status = serializers.ReadOnlyField(source="fk_employee_user.status")
    profile_id = serializers.ReadOnlyField(source="profile.id")
    profile_description = serializers.ReadOnlyField(source="profile.description")

    class Meta:
        model = User
        fields = (
            "user_id",
            "username",
            "is_active",
            "employee_id",
            "names",
            "lastnames",
            "status",
            "profile_id",
            "profile_description",
        )
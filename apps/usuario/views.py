from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import TemplateHTMLRenderer
from django.db import transaction

from apps.user.serializers import UserSerializer
from .models import *
from .serializers import *
from .filters import *

import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse

class UsuarioView(viewsets.GenericViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuarioFilter
    pagination_class = UsuarioPagination

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
            user_serializer = UserSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['PUT'])
    def change_password(self, request, pk=None):
        instance = self.get_object()
        user = instance.user
        new_password = request.data.get('password', None)
        if not new_password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        instance = self.get_object()
        instance.status = request.data.get('status', None)
        user_session = Token.objects.filter(user=instance.user.id)
        if user_session.exists():
            user_session.delete()
        instance.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], renderer_classes=[TemplateHTMLRenderer])
    def report(self, request, *args, **kwargs):
        params = request.query_params.dict()

        queryset = self.filter_queryset(self.get_queryset().order_by('id'))
        data = {
            "usuarios": queryset,
            "counter": 0,
            "params": params,
        }
        # return Response(data, template_name='./lista_usuarios.html', status=status.HTTP_200_OK)
       
        html = render_to_string('lista_usuarios.html', data)
        pdf_file = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=pdf_file)
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Reporte_de_usuarios.pdf"'
        return response
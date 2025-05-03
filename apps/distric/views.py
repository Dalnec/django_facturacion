from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import *
from .serializers import *
from .filters import *

@extend_schema(tags=["Distric"])
class DistricView(viewsets.GenericViewSet):
    serializer_class = DistricSerializer
    queryset = Distric.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DistricFilter
    pagination_class = DistricPagination

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
    
    @action(detail=True, methods=['get'], serializer_class=SettingsSerializer)
    def get_settings(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance.settings)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['put'], serializer_class=SettingsSerializer)
    def update_settings(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance.settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.settings = serializer.validated_data
        instance.save()
        return Response({**instance.settings},status=status.HTTP_200_OK)
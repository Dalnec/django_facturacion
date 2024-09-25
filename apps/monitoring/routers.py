# Routers for app: monitoring
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MonitoringView

router = DefaultRouter()
router.register(r'monitoring', MonitoringView, basename='monitoring')

urlpatterns = router.urls
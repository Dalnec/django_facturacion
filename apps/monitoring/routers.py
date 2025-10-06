# Routers for app: monitoring
from rest_framework.routers import DefaultRouter
from .views import MonitoringView

router = DefaultRouter()
router.register(r'monitoring', MonitoringView, basename='monitoring')

urlpatterns = router.urls
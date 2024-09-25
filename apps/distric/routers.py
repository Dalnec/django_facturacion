# Routers for app: distric
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DistricView

router = DefaultRouter()
router.register(r'distric', DistricView, basename='distric')

urlpatterns = router.urls
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SeedingView
router = DefaultRouter()

router.register(r'init-data', SeedingView, basename="InitData")
urlpatterns = router.urls
# Routers for app: usuario
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsuarioView

router = DefaultRouter()
router.register(r'usuario', UsuarioView, basename='usuario')

urlpatterns = router.urls

# Routers for app: usuario
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsuarioView, UsuarioDetailView

router = DefaultRouter()
router.register(r'usuario', UsuarioView, basename='usuario')
router.register(r'usuariodetail', UsuarioDetailView, basename='usuariodetail')

urlpatterns = router.urls

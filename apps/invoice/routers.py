# Routers for app: invoice
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import InvoiceView

router = DefaultRouter()
router.register(r'invoice', InvoiceView, basename='invoice')

urlpatterns = router.urls
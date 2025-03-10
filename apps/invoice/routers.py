# Routers for app: invoice
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import InvoiceView, InvoiceTicketView

router = DefaultRouter()
router.register(r'invoice', InvoiceView, basename='invoice')

urlpatterns = [
    path("", include(router.urls)),
    path('ticket/<uuid:uuid>/', InvoiceTicketView.as_view(), name='invoice-ticket'),
]
# Routers for app: purchase
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PurchaseView

router = DefaultRouter()
router.register(r'purchase', PurchaseView, basename='purchase')

urlpatterns = router.urls

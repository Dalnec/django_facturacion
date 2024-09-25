# Routers for app: user
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EmployeeView, UserView, ProfileView

router = DefaultRouter()
router.register(r'user', UserView, basename='user')
router.register(r'profile', ProfileView, basename='profile')
router.register(r'employee', EmployeeView, basename='employee')
urlpatterns = router.urls
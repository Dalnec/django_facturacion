from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.user.views import Login, Logout

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url=reverse_lazy("admin:index"))),
    # apps
    path("api/login/", Login.as_view(), name="login"),
    path("api/logout/", Logout.as_view(), name="logout"),
    path('api/', include('apps.seeder.routers'), name='seeder'),
    path('api/', include('apps.distric.routers'), name='distric'),
    path('api/', include('apps.invoice.routers'), name='invoice'),
    path('api/', include('apps.monitoring.routers'), name='monitoring'),
    path('api/', include('apps.purchase.routers'), name='purchase'),
    path('api/', include('apps.user.routers'), name='user'),
    path('api/', include('apps.usuario.routers'), name='usuario'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
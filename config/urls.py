"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('products/', include('products.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('orders/', include('orders.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/Logout
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

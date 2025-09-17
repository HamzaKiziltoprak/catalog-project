
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import redirect_to_employees

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('contact/', redirect_to_employees, name='redirect_to_employees'),
]


# Media dosyaları için URL yapılandırması
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

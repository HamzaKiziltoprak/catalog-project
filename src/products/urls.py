from django.urls import path
from .views import home_view,product_list_view,product_detail_view

# product_list_view(request) → ürünleri listeler, kategori filtreleme ile 
# product_detail_view(request, slug) → ürün detay + görseller + sepete ekle formu

app_name = 'product'  # Uygulama ad alanı, URL isimlendirmede kullanılır

urlpatterns = [
    path('', home_view, name='home'),
    path('products/', product_list_view, name='product_list'),
    path('products/<slug:slug>/', product_detail_view, name='product_detail'),  # Detay sayfası için
]

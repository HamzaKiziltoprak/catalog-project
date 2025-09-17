from django.shortcuts import render,get_object_or_404
from .models import Product, Category, ProductImage 
import requests

def home_view(request):
    popular_products = Product.objects.all().distinct()  # Her ürünün birden fazla fotoğrafı olabilir, hepsini getirir
    context = {
        'popular_products': popular_products
    }
    print(context)
    return render(request, 'home.html', context)



def product_list_view(request):
    # Başlangıçta aktif ürünleri al
    products = Product.objects.filter(is_active=True).prefetch_related('images', 'category')
    categories = Category.objects.filter(is_active=True)
    
    # Kategori filtresi
    selected_category_ids = request.GET.getlist('category')
    if selected_category_ids:
        # String'leri integer'a çevir ve filtrele
        try:
            category_ids = [int(cat_id) for cat_id in selected_category_ids if cat_id.isdigit()]
            if category_ids:
                products = products.filter(category__id__in=category_ids).distinct()
        except (ValueError, TypeError):
            # Hatalı kategori ID'leri varsa göz ardı et
            pass
    
    # İsim filtresi
    name_filter = request.GET.get('name', '').strip()
    if name_filter:
        products = products.filter(name__icontains=name_filter)
    
    # Fiyat filtreleri
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    currency_filter = request.GET.get('currency')
    
    # Para birimi filtresi
    if currency_filter and currency_filter in ['USD', 'EUR', 'TRY']:
        products = products.filter(currency=currency_filter)
    
    # Minimum fiyat filtresi
    if min_price:
        try:
            min_price_decimal = float(min_price)
            if min_price_decimal >= 0:
                products = products.filter(price__gte=min_price_decimal)
        except (ValueError, TypeError):
            # Hatalı fiyat değeri varsa göz ardı et
            pass
    
    # Maksimum fiyat filtresi  
    if max_price:
        try:
            max_price_decimal = float(max_price)
            if max_price_decimal >= 0:
                products = products.filter(price__lte=max_price_decimal)
        except (ValueError, TypeError):
            # Hatalı fiyat değeri varsa göz ardı et
            pass
    
    # Fiyat tutarlılık kontrolü
    error_message = None
    if min_price and max_price:
        try:
            min_val = float(min_price)
            max_val = float(max_price)
            if min_val > max_val:
                error_message = "Minimum fiyat, maksimum fiyattan büyük olamaz."
        except (ValueError, TypeError):
            pass
    
    # Integer'a çevirme işlemi (template için)
    try:
        selected_category_ids_int = [int(cat_id) for cat_id in selected_category_ids if cat_id.isdigit()]
    except (ValueError, TypeError):
        selected_category_ids_int = []
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category_ids': selected_category_ids_int,
        'error': error_message,
        # Template'te aktif filtreleri göstermek için GET parametrelerini de gönder
        'request': request,
    }
    
    return render(request, 'product/product_list_view.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('images', 'category'),
        slug=slug,
        is_active=True
    )

    context = {
        'product': product,
        'images': product.images.filter(is_active=True).order_by('order')
    }
    print(context)
    return render(request, 'product/product_detail_view.html', context)

from django.shortcuts import render,get_object_or_404,redirect
from .utils.cart import Cart
from .models import Order, OrderItem
from products.models import Product
from admin_side.models import ContactNumber




def cart_add_view(request,slug,quantity=1):
    cart = Cart(request)
    
    product = get_object_or_404(Product, slug=slug, is_active=True)

    cart.add(product,quantity)
    return redirect('orders:cart_detail')

def cart_remove_view(request,slug):
    cart = Cart(request)
    product = get_object_or_404(Product,slug=slug,is_active=True)

    cart.remove(product)
    return redirect('orders:cart_detail')

def update_cart_view(request,slug,quantity):
    cart = Cart(request)
    product = get_object_or_404(Product,slug=slug,is_active=True)

    cart.update(product,quantity)
    return redirect('orders:cart_detail')

def cart_clear_view(request):
    cart = Cart(request)
    cart.clear()
    return redirect('orders:cart_detail')

def cart_detail_view(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    
    return render(request, 'cart/cart_detail.html', context)

def checkout_view(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        person_info = request.POST.get('name')
        person_info = person_info.strip().split(" ")
        name = person_info[0]
        surname = person_info[1] if len(person_info) > 1 else None

        if not name:
            return redirect('orders:cart_detail')
        
        if not surname:
            surname = None
            
    
        if not request.session.session_key:
            request.session.create()
            
        order = Order.objects.create(
            session_key=request.session.session_key,
            name=name,
            # surname=surname
        )
        
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity']
            )

        contact = ContactNumber.objects.filter(is_active=True).order_by('?').first()
        phone_number = contact.phone_number if contact else None
        if surname is None:
            content = f"merhablar {contact.name},\nBen {name} ve sipariş numaram {order.id}\nSipariş etmek istediğim Ürünler:\n {' - '.join([f'{item['product'].name} (x{item['quantity']})' for item in cart]) }\nYardımcı olabilir misiniz?"
        else:
            content = f"merhablar {contact.name},\nBen {name} {surname} ve sipariş numaram {order.id}\nSipariş etmek istediğim Ürünler:\n {' -  '.join([f'{item['product'].name} ( x{item['quantity']} )' for item in cart]) }\nYardımcı olabilir misiniz?"
        cart.clear()
        
        # WhatsApp'a yönlendirilsin ve ana sayfaya dönsün
        import urllib.parse
        from django.shortcuts import redirect

        if phone_number:
            # '+' işaretini kaldır
            phone_number = phone_number.lstrip('+')
            message = urllib.parse.quote(content)
            whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
            return redirect(whatsapp_url)
        else:
            return redirect('product_list_view')

    
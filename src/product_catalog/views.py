from django.shortcuts import redirect
import urllib.parse
from products.models import Product, Category, ProductImage
from admin_side.models import ContactNumber

app_name = 'product_catalog'        

def redirect_to_employees(request):

    contact = ContactNumber.objects.filter(is_active=True).order_by('?').first()
    phone_number = contact.phone_number if contact else None
    
    if phone_number:
        phone_number = phone_number.lstrip('+')
        message = urllib.parse.quote("")
        whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
        return redirect(whatsapp_url)
    else:
        return redirect('product_list_view')

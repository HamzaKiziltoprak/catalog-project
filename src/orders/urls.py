from django.urls import path
from .views import (
    cart_add_view,
    cart_remove_view,
    update_cart_view,
    cart_clear_view,
    cart_detail_view,
    checkout_view
)

app_name = 'orders'

urlpatterns = [
    path("cart/add/<slug:slug>/<int:quantity>/", cart_add_view, name="cart_add"), #cart_add_view(request, slug, quantity=1)
    path("cart/remove/<slug:slug>/",cart_remove_view,name="cart_remove"), #cart_remove_view(request, slug)
    path("cart/update/<slug:slug>/<int:quantity>/",update_cart_view,name="cart_update"), #update_cart_view(request, slug, quantity)
    path("cart/clear/",cart_clear_view,name="cart_clear"), #cart_clear_view(request)
    path("cart/",cart_detail_view,name="cart_detail"), #cart_detail_view(request)
    path("checkout/",checkout_view,name="checkout"), #checkout_view(request)
]


from django.db import models
from products.models import Product, TimestampedModel

class Order(TimestampedModel):
    session_key = models.CharField(max_length=40, verbose_name="Session ID")
    name = models.CharField(max_length=100, verbose_name="Müşteri Adı")
    surname = models.CharField(max_length=100, blank=True,null=True,verbose_name="Müşteri Soyadı", default="")
    def __str__(self):
        return f"{self.name} - {self.session_key}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
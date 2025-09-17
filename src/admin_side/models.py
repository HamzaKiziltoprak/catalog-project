from django.db import models
from products.models import TimestampedModel
from django.core.exceptions import ValidationError
import re


class ContactNumber(TimestampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="İsim")
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="WhatsApp Telefon Numarası",
        help_text="Format: + 90xxxxxxxxxx"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        verbose_name = "İletişim Ayarı"
        verbose_name_plural = "İletişim Ayarları"

    def __str__(self):
        return f"{self.name} - {self.phone_number}--{'Aktif' if self.is_active else 'Pasif'}"
    
    def clean(self):
        super().clean()
        if not re.match(r'^\+90\d{10}$', self.phone_number):
            raise ValidationError({'phone_number': "Telefon numarası '+90xxxxxxxxxx' formatında olmalıdır."})
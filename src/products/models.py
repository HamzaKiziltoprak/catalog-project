from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage


class TimestampedModel(models.Model):
    """Base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        abstract = True


class Category(TimestampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL Slug")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    
    class Meta:
        verbose_name = "kategori"
        verbose_name_plural = "kategoriler"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product(TimestampedModel):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('TRY', 'Turkish Lira'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Ürün Adı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL Slug")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Kategori"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Fiyat"
    )  # max 99999999.99
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='TRY',
        verbose_name="Para Birimi"
    )
    
    class Meta:
        verbose_name = "ürün"
        verbose_name_plural = "ürünler"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # category-name-product-name şeklinde slug oluştur
            self.slug = slugify(f"{self.category.name}-{self.name}")
        if not self.category.is_active:
            self.is_active = False
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class ProductImage(TimestampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',  # product.images.all() yapınca o ürüne ait tüm resimleri getirir
        verbose_name="Ürün"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    image = models.ImageField(
        upload_to='django_products_images/',
        storage=MediaCloudinaryStorage(),
        verbose_name="Ürün Görseli"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "ürün görseli"
        verbose_name_plural = "ürün görselleri"
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.product.name} - Görsel {self.id}"
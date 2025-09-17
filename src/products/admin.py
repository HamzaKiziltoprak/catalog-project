from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    list_filter = ('is_active', 'created_at')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


class ProductImageInline(admin.TabularInline):
    """Ürün sayfasında görselleri inline olarak göster"""
    model = ProductImage
    extra = 1  # Boş bir form daha göster
    fields = ('image_preview', 'image', 'is_active', 'order')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:8px;border:2px solid #ddd;" />'
                '</a>',
                obj.image.url,
                obj.image.url
            )
        return "❌"
    image_preview.short_description = 'Önizleme'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'currency', 'slug', 'is_active', 'image_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_active', 'currency', 'created_at')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    # Ürün formunda görselleri inline olarak göster
    inlines = [ProductImageInline]
    
    # Fieldsets ile formu organize et
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Fiyat Bilgisi', {
            'fields': ('price', 'currency')
        }),
        ('Durum', {
            'fields': ('is_active',)
        }),
        ('Zaman Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Başlangıçta kapalı
        }),
    )
    
    def image_count(self, obj):
        """Ürünün kaç görselinin olduğunu göster"""
        count = obj.images.filter(is_active=True).count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">📷 {}</span>',
                count
            )
        return format_html('<span style="color: red;">❌ 0</span>')
    image_count.short_description = 'Görseller'


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_active', 'order', 'created_at')
    list_display_links = ('product',)
    search_fields = ('product__name',)
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active', 'order')  # Liste sayfasında direkt düzenlenebilir
    ordering = ('product', 'order')
    readonly_fields = ('created_at', 'updated_at', 'image_preview_large')
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('product', 'image', 'image_preview_large')
        }),
        ('Ayarlar', {
            'fields': ('is_active', 'order'),
            'classes': ('wide',)
        }),
        ('Zaman Bilgileri', {
            'fields': (('created_at', 'updated_at'),),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """Admin listesinde küçük görsel önizlemesi"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 2px solid #ddd;" />',
                obj.image.url
            )
        return "❌"
    image_preview.short_description = 'Önizleme'
    
    def image_preview_large(self, obj):
        """Form sayfasında büyük görsel önizlemesi"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: cover; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />',
                obj.image.url
            )
        return "Henüz görsel yüklenmedi"
    image_preview_large.short_description = 'Büyük Önizleme'


# Admin kayıtları
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)

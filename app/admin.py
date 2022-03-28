from django.contrib import admin

from .models import (Customer, Product, Cart, OrderPlaced)

# Register your models here.

# admin.site.register(Customer)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']


# admin.site.register(Product)
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']


# admin.site.register(Cart)
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


from django.urls import reverse
from django.utils.html import format_html
# admin.site.register(OrderPlaced)
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_info', 'product', 'quantity', 'ordered_date', 'status']
    
    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
    
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
from django.contrib import admin
from .models import Customer, Order, OrderItem, Product, ShippingAddress
from django.contrib.auth.models import User

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ('user', 'name', 'email')
    list_display = ('user', 'name', 'email')
    ordering = ('name',)
    search_fields = ('name',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('customer', 'complete', 'transaction_id')
    list_display = ('customer', 'date_ordered', 'complete', 'transaction_id')
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    fields = ('product', 'order', 'quantity')
    list_display = ('product', 'order', 'quantity', 'date_added')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'price', 'digital', 'image')
    list_display = ('name', 'price', 'digital', 'image')
    ordering = ('name',)
    search_fields = ('name',)
    
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    fields = ('customer', 'order', 'address', 'city', 'state', 'zip_code')
    list_display = ('customer', 'address', 'city', 'state', 'zip_code')
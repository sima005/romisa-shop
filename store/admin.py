from django.contrib import admin
from .models import Category, ContactMessage, Order, OrderItem, Product, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug','active'); list_filter=('active',); search_fields=('name',); prepopulated_fields={'slug':('name',)}

class VariantInline(admin.TabularInline):
    model=ProductVariant; extra=1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','base_price','discount_percent','featured','active','created_at')
    list_filter=('category','featured','active'); search_fields=('name','fabric','description'); prepopulated_fields={'slug':('name',)}
    inlines=[VariantInline]
    fieldsets=((None,{'fields':('name','slug','category','description','fabric','image')}),('قیمت و فروش',{'fields':('base_price','discount_percent','featured','active')}))

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display=('product','color_name','color_hex','price','stock','active'); list_filter=('active','product'); search_fields=('product__name','color_name')

class OrderItemInline(admin.TabularInline):
    model=OrderItem; extra=0; readonly_fields=('unit_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','customer_name','phone','total','status','created_at'); list_filter=('status','created_at'); search_fields=('customer_name','phone'); inlines=[OrderItemInline]

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display=('name','contact','read','created_at'); list_filter=('read','created_at'); search_fields=('name','contact','message')

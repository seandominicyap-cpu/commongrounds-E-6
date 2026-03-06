from django.contrib import admin
from .models import ProductType, Product


class ProductInline(admin.TabularInline):
    model = Product


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [ProductInline]


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("name", "product_type", "price")
    list_filter = ("product_type",)


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)

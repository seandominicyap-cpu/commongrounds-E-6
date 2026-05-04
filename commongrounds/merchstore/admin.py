from django.contrib import admin
from .models import ProductType, Product, Transaction


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [ProductInline]
    search_fields = ("name",)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("name", "product_type", "price", "stock", "status", "owner")
    list_filter = ("status", "product_type")
    search_fields = ("name", "description")


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ("product", "amount", "buyer", "status", "created_on")
    list_filter = ("status", "created_on")
    search_fields = ("product__name", "buyer__user__username")


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)

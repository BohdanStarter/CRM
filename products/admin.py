from django.contrib import admin
from products.models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "status", "updated_at", "created_at"]
    list_filter = ["status", "category", "billing_type"]
    search_fields = ["name", "description"]


admin.site.register(Product, ProductAdmin)
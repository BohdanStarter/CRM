from django.contrib import admin
from licenses.models import License
# Register your models here.

class LicenseAdmin(admin.ModelAdmin):
    ordering = ["product__name"]
    list_display = ["customer__full_name", "product__name", "license_key", "status", "expiration_date"]
    list_filter = ["status", "product__name", "customer__full_name", "expiration_date"]
    search_fields = ["customer__full_name", "product__name", "license_key"]
    exclude = ["expiration_date"]


admin.site.register(License, LicenseAdmin)
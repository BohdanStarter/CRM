from django.contrib import admin
from customers.models import Customer
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    ordering = ["full_name"]
    list_display = ["full_name", "email", "status", "updated_at", "created_at"]
    list_filter = ["full_name", "email", "status"]
    search_fields = ["full_name", "email", "phone_number"]


admin.site.register(Customer, CustomerAdmin)
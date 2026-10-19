from django.contrib import admin
from activity.models import Activity
# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_select_related = ["created_by", "customer", "related_license__product"]
    list_display = ["customer__full_name", "activity_type", "subject", "related_license__product__name", "occurred_at", "created_by"]
    list_filter = ["created_by", "created_at", "occurred_at", "activity_type"]
    search_fields = ["customer__full_name", "customer__email", "related_license__product__name", "subject", "description"]
    readonly_fields = ["created_by", "updated_by", "created_at", "updated_at"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Activity, ActivityAdmin)
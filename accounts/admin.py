from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User

class UserAdmin(BaseUserAdmin):
    ordering = ["username"]
    list_display = ["username", "email", "first_name", "last_name", "role", "is_staff"]
    list_filter = ["role", "is_staff", "is_superuser", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]

    @property
    def fieldsets(self):
        modified_fieldsets = []
        for name, field_options in BaseUserAdmin.fieldsets:
            if name == 'Permissions':
                fields = tuple(f for f in field_options['fields'] if f != 'groups')
                modified_fieldsets.append((name, {'fields': fields}))
            else:
                modified_fieldsets.append((name, field_options))

        # Inject your custom role field layout
        return tuple(modified_fieldsets) + (
            ("Custom Role", {"fields": ("role",)}),
        )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Custom Role", {"fields": ("role",)}),
    )

admin.site.register(User, UserAdmin)
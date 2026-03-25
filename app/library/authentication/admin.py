from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'middle_name', 'role_name', 'is_staff', 'is_superuser', 'is_active', 'created_at', 'updated_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups', 'created_at', 'updated_at')
    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'middle_name', 'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

    def role_name(self, obj):
        return obj.get_role_display()

    role_name.short_description = 'Role'

from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_book_name',
        'get_user_email',
        'created_at',
        'plated_end_at',
        'end_at',
        'get_status',
    )
    list_filter = ('end_at', 'created_at', 'plated_end_at')
    search_fields = ('book__name', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'get_status')

    fieldsets = (
        ('Order Info', {
            'fields': ('book', 'user'),
        }),
        ('Dates', {
            'fields': ('created_at', 'plated_end_at', 'end_at'),
        }),
        ('Status', {
            'fields': ('get_status',),
        }),
    )

    def get_book_name(self, obj):
        return obj.book.name
    get_book_name.short_description = 'Book'

    def get_user_email(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name} ({obj.user.email})"
    get_user_email.short_description = 'User'

    def get_status(self, obj):
        if obj.end_at is None:
            return 'Not returned'
        return 'Returned'
    get_status.short_description = 'Status'

from django.contrib import admin
from order.models import Order
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'count', 'get_authors')
    list_filter = ('id', 'name', 'authors__name', 'authors__surname', 'authors__patronymic')
    search_fields = ('=id', 'name', 'description', 'authors__name', 'authors__surname')
    ordering = ('name',)

    readonly_fields = ('get_active_order_info',)

    fieldsets = (
        ('Static Data', {'fields': ('name', 'authors', 'description')}),
        ('Changing Data', {'fields': ('count',)}),
        ('Current Order Status', {'fields': ('get_active_order_info',)}),
    )

    def get_authors(self, obj):
        return ", ".join([f"{author.name} {author.surname}" for author in obj.authors.all()])
    get_authors.short_description = 'Authors'

    def get_active_order_info(self, obj):
        active_orders = Order.objects.filter(book=obj, end_at__isnull=True).order_by('-created_at')
        if not active_orders.exists():
            return 'Available now (no active orders)'

        details = []
        for order in active_orders:
            user = order.user
            details.append(
                f"{user.first_name} {user.last_name} ({user.email}) since {order.created_at:%Y-%m-%d %H:%M}, planned return: {order.plated_end_at:%Y-%m-%d %H:%M}"
            )

        return f"Active orders: {active_orders.count()}. " + '; '.join(details)

    get_active_order_info.short_description = 'Order info'

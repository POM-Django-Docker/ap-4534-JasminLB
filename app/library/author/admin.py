from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'get_books_count')
    list_filter = ('name', 'surname', 'patronymic')
    search_fields = ('name', 'surname', 'patronymic')
    ordering = ('surname', 'name')
    readonly_fields = ('get_books_list',)

    fieldsets = (
        (None, {'fields': ('name', 'surname', 'patronymic')}),
        ('Books', {'fields': ('get_books_list',)}),
    )

    def get_books_count(self, obj):
        return obj.books.count()
    get_books_count.short_description = 'Books Count'

    def get_books_list(self, obj):
        return ", ".join(f"{book.id}: {book.name}" for book in obj.books.order_by('id')) or 'No books'
    get_books_list.short_description = 'Linked books'

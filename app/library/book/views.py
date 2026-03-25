from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from authentication.decorators import role_required
from author.models import Author
from .forms import BookForm
from .models import Book
from .serializers import BookSerializer


@role_required(0, 1)
def book_list(request):
    name = request.GET.get("name", "").strip()
    author = request.GET.get("author", "").strip()

    books = Book.get_all()

    if name:
        books = books.filter(name__icontains=name)

    if author:
        books = books.filter(
            Q(authors__name__icontains=author)
            | Q(authors__surname__icontains=author)
            | Q(authors__patronymic__icontains=author)
        )

    authors = Author.objects.all().order_by("surname", "name")

    return render(
        request,
        "book/book_list.html",
        {
            "books": books.distinct().order_by("id"),
            "authors": authors,
            "name": name,
            "author": author,
        },
    )


@role_required(0, 1)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    return render(
        request,
        "book/book_detail.html",
        {
            "book": book,
        },
    )


@role_required(1)
@require_http_methods(["GET", "POST"])
def book_admin_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(initial={"count": 10})

    return render(request, "book/book_admin_create.html", {"form": form})


@role_required(1)
@require_http_methods(["GET", "POST"])
def book_admin_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "book/book_admin_update.html",
        {
            "book": book,
            "form": form,
        },
    )


@role_required(1)
@require_http_methods(["POST"])
def book_admin_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer

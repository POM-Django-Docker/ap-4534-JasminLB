from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, status
from rest_framework.response import Response
from authentication.decorators import role_required
from .forms import AuthorForm
from .models import Author
from .serializers import AuthorSerializer


@role_required(1)
def author_admin_list(request):
    authors = Author.get_all().order_by("id")
    return render(request, "author/author_admin_list.html",
                  {"authors": authors})

@role_required(1)
@require_http_methods(["GET", "POST"])
def author_admin_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("author_admin_list")
    else:
        form = AuthorForm()

    return render(
        request,
        "author/author_admin_create.html",
        {"form": form},
    )


@role_required(1)
@require_http_methods(["GET", "POST"])
def author_admin_update(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect("author_admin_list")
    else:
        form = AuthorForm(instance=author)

    return render(
        request,
        "author/author_admin_update.html",
        {
            "form": form,
            "author": author,
        },
    )


@role_required(1)
@require_http_methods(["POST"])
def author_admin_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if author.books.exists():
        authors = Author.get_all().order_by("id")
        return render(
            request,
            "author/author_admin_list.html",
            {
                "authors": authors,
                "error": "Cannot delete author because this author is linked to a book.",
            },
        )

    author.delete()
    return redirect("author_admin_list")


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("id")
    serializer_class = AuthorSerializer

    def destroy(self, request, *args, **kwargs):
        author = self.get_object()

        if author.books.exists():
            return Response(
                {
                    "error_code": 300,
                    "message": "It is not possible to delete an author who has books."},
                status=status.HTTP_400_BAD_REQUEST
            )

        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
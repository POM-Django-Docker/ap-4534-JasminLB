from django import forms

from author.models import Author
from .models import Book


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all().order_by("surname", "name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Book
        fields = ["name", "description", "count", "authors"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "128",
                    "placeholder": "Enter book name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "maxlength": "256",
                    "placeholder": "Enter book description",
                    "rows": 4,
                }
            ),
            "count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter number of copies",
                }
            ),
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()

        if not name:
            raise forms.ValidationError("Name is required.")

        return name

    def clean_count(self):
        count = self.cleaned_data["count"]

        if count < 0:
            raise forms.ValidationError("Count cannot be negative.")

        if count > 500:
            raise forms.ValidationError("Count too much.")

        return count

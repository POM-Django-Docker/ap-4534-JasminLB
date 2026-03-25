from django import forms

from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "surname", "patronymic"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter name",
                    "maxlength": "20",

                }
            ),
            "surname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter surname",
                    "maxlength": "20",
                }
            ),
            "patronymic": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter patronymic",
                    "maxlength": "20",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        name = (cleaned_data.get("name") or "").strip()
        surname = (cleaned_data.get("surname") or "").strip()
        patronymic = (cleaned_data.get("patronymic") or "").strip()

        cleaned_data["name"] = name
        cleaned_data["surname"] = surname
        cleaned_data["patronymic"] = patronymic

        if name and surname and patronymic:
            qs = Author.objects.filter(
                name__iexact=name,
                surname__iexact=surname,
                patronymic__iexact=patronymic
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Author with these details already exists."
                )

        return cleaned_data

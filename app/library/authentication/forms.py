from django import forms

ROLE_CHOICES = (
    (0, "Visitor"),
    (1, "Librarian"),
)

class RegisterForm(forms.Form):

    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "John"
        })
    )

    last_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Doe"
        })
    )

    middle_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Middle Name"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "email@example.com"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********"
        })
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )
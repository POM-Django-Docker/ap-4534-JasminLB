from django import forms

class OrderCreateForm(forms.Form):
    confirm = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )


class OrderCloseForm(forms.Form):
    confirm = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):

    # remove help text
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        #adds form-control to forms for formatting
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class']='form-control'

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    first_name = forms.CharField(max_length=50, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=50, required=False, help_text="Optional")
    email = forms.EmailField(max_length=254)
    discord = forms.CharField(max_length=50, required=False, help_text="Optional")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "discord",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
        }

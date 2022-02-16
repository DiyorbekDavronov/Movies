from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, password_validation, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from .models import Film


# ModelForm - форма связанная с моделью
# Form - обычная форма

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ("title", "description", "image", "category", "is_published")
        # exclude
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control"
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            })
        }


# Аутенфикация
# Авторизация
class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            "class": "form-control"
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            "class": "form-control"
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            })
        }


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        "class": "form-control"
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            "class": "form-control"
        }),
    )

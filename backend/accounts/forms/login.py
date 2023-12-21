from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(), label=_('E-mail'))
    password = forms.CharField(widget=forms.PasswordInput(), label=_('Password'))

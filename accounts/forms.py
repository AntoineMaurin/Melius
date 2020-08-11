from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(forms.Form):
    email = forms.EmailField(max_length=100)
    pw1 = forms.CharField(max_length=32,
                          label='Mot de passe',
                          widget=forms.PasswordInput)
    pw2 = forms.CharField(max_length=32,
                          label='Confirmation mot de passe',
                          widget=forms.PasswordInput)


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=100,
                                label='Email')
    password = forms.CharField(max_length=32,
                               label='Mot de passe',
                               widget=forms.PasswordInput)

from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
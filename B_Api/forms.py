from django import forms
from django.contrib.auth.forms import AuthenticationForm 
from .models import Publishable

class PublishableForm(forms.ModelForm):

    class Meta:
        model = Publishable
        fields = ('name', 'description',)
        abstract=True 



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'type':'text', 'name': 'username', 'placeholder':'User name'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.TextInput(attrs={'type':'password', 'name': 'password', 'placeholder':'Password'}))












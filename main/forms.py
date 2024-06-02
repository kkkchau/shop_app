from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'required': True}),
            'phone_number': forms.TextInput(attrs={'required': True}),
            'address': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
        }

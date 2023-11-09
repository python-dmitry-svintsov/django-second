from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'order-elem',
            'placeholder': 'имя'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'order-elem',
            'placeholder': 'фамилия'
        })
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'order-elem',
            'placeholder': 'email'
        })
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'order-elem',
            'placeholder': 'адресс'
        })
    )
    postal_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'order-elem',
            'placeholder': 'почтовый код'
        })
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'order-elem',
            'placeholder': 'город'
        })
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
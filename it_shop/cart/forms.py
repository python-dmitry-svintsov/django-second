from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class Product_Add_Form(forms.Form):
    # quantity = forms.TypedChoiceField(coerce=int, widget=forms.NumberInput(attrs={
    #     'class': 'integer-input',
    #     'min': 1,
    #     'max': '{{ book.quantity }}',
    #     'value': 1
    # }))
    quantity = forms.CharField(widget=forms.NumberInput())
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


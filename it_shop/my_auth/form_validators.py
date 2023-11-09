from django import forms
from django.core import validators


class My_radio_fields(forms.IntegerField):
    def to_python(self, value):
        if not value:
            return 1
        return value

    def validate(self, value):
        validators.integer_validator(value)

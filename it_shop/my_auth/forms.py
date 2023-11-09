from django.contrib.auth.forms import UserCreationForm, forms, UserChangeForm
from .models import Sex
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model, password_validation


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'class': 'input-elem',
            'placeholder': 'username'
        })
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'input-elem',
            'placeholder': 'email'
        })
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'input-elem',
            'placeholder': 'новый пароль'
        }),
        help_text=password_validation.password_validators_help_texts()
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'input-elem',
            'placeholder': 'повторите пароль'
        }),
        help_text=password_validation.password_validators_help_texts()
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)


class User_Profile_Update_Form(UserChangeForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'input-elem',
            'placeholder': 'email'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'first_name',
            'class': 'input-elem',
            'placeholder': 'имя'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'last_name',
            'class': 'input-elem',
            'placeholder': 'фамилия'
        })
    )
    surname = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'surname',
            'class': 'input-elem',
            'placeholder': 'отчество'
        })
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'city',
            'class': 'input-elem',
            'placeholder': 'город'
        })
    )
    sex = forms.ModelChoiceField(label='пол', widget=forms.RadioSelect, queryset=Sex.objects.all())
    photo = forms.ImageField(widget=forms.ClearableFileInput)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email', 'last_name', 'surname', 'city', 'sex', 'photo')


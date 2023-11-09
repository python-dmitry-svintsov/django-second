from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager


class Sex(models.Model):
    male = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.male


class MyUser(AbstractUser):
    username = models.CharField(unique=True, max_length=25, verbose_name='никнейм')
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    surname = models.CharField(max_length=25, null=True, blank=True, verbose_name='отчество')
    phone = PhoneNumberField(unique=True, null=True, blank=True, verbose_name='телефон')
    photo = models.ImageField(upload_to='profile/users', null=True, blank=True, verbose_name='фотография')
    city = models.CharField(max_length=25, null=True, blank=True, verbose_name='город')
    sex = models.ForeignKey(Sex, on_delete=models.PROTECT, default=1, verbose_name='пол')
    slug = AutoSlugField(populate_from='username', verbose_name='URL')

    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse_lazy('my_auth:profile', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = '-is_superuser', '-is_active'

    def __str__(self):
        return self.username
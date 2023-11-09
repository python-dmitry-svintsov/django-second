from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.contrib.auth.models import Group


@admin.register(models.MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'password']
    ordering = ['username']
    # prepopulated_fields = {"slug": ("username", )}
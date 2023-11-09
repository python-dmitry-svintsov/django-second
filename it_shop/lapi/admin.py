from django.contrib import admin
from .models import Lapi


@admin.register(Lapi)
class Lapi_Admin(admin.ModelAdmin):
    list_display = ['title', 'difficult', 'difficult', 'max_enemys', 'speed', 'map', 'slug']
    ordering = ('title',)

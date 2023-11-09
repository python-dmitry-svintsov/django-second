from django.contrib import admin
from .models import Levels


@admin.register(Levels)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'difficult', 'max_enemys', 'speed', 'slug']
    ordering = ['level']
    # prepopulated_fields = {"slug": ("title", )}

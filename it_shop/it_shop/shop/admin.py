from django.contrib import admin
from . import models


@admin.register(models.It_Book)
class It_Book_Admin(admin.ModelAdmin):
    list_display = ['title', 'description', 'pubhouse', 'year', 'book_id', 'isbn', 'pages',
                    'dimension', 'weight', 'authors', 'artists', 'price', 'icon',
                    'demo_pdf', 'quantity', 'available']
    ordering = ['title', 'year']
    search_fields = ['title']

    def short_description(self, obj: models.It_Book):
        if len(obj.description) < 12:
            return obj.description
        else:
            return obj.description[:9] + '...'


@admin.register(models.Categories)
class Categories_Admin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'icon', 'slug']
    ordering = ['name']
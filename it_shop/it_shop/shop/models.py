from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField('название', max_length=50)
    description = models.TextField('описание')
    quantity = models.IntegerField('количество', default=0)
    icon = models.ImageField(upload_to='categories', null=True, blank=True, verbose_name='icons')
    slug = AutoSlugField(populate_from='name', verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class It_Book(models.Model):
    title = models.CharField('название', max_length=250)
    description = models.TextField('описание')
    pubhouse = models.CharField('издательство', max_length=50)
    year = models.IntegerField('год')
    book_id = models.IntegerField('id')
    isbn = models.CharField('isbn', max_length=50)
    pages = models.IntegerField('страниц')
    dimension = models.CharField('размеры', max_length=25)
    weight = models.IntegerField('вес')
    authors = models.CharField('автор(ы)', max_length=250)
    artists = models.CharField('художник(и)', max_length=100)
    price = models.IntegerField('цена')
    icon = models.ImageField(upload_to='it_books/img', null=True, blank=True, verbose_name='обложка')
    demo_pdf = models.ImageField(upload_to='it_books/pdf', null=True, blank=True, verbose_name='demo')
    quantity = models.IntegerField('количество', default=100)
    available = models.BooleanField('доступность', default=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'


class More_Photo_It_books(models.Model):
    book = models.ForeignKey(It_Book, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='profile/users', null=True, blank=True, verbose_name='картинка')

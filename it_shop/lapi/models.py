import os.path
import sys

from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse_lazy

def printing(data):
    print(data, file=sys.stdout)


class Lapi(models.Model):
    title = models.CharField(verbose_name='наименование', max_length=25)
    difficult = models.IntegerField(verbose_name='сложность')
    max_enemys = models.IntegerField(verbose_name='макс. кол. врагов')
    speed = models.IntegerField(verbose_name='скорость спауна врагов')
    map = models.FileField(upload_to='lapi/levels/', verbose_name='уровень')
    style = models.IntegerField(verbose_name='style', blank=True, null=True)
    background = models.ImageField(upload_to='lapi/backgrounds/', blank=True, null=True, verbose_name='фон')
    slug = AutoSlugField(populate_from='title', verbose_name='URL')

    def get_absolute_url(self):
        return reverse_lazy('tank:game', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'уровень'
        verbose_name_plural = 'уровни'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_map(self):
        with open(f'./media/{self.map}') as f:
            data = f.readlines()
            for ind, row in enumerate(data):
                data[ind] = list(map(lambda x: int(x), row.strip().split()))
        return data


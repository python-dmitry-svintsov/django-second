from django.db import models
from django.urls import reverse_lazy
from autoslug import AutoSlugField


class Levels(models.Model):
    title = models.CharField(verbose_name='наименование', max_length=25)
    level = models.IntegerField(verbose_name='уровень')
    difficult = models.IntegerField(verbose_name='сложность')
    max_enemys = models.IntegerField(verbose_name='макс. кол. врагов')
    speed = models.IntegerField(verbose_name='скорость спауна врагов')
    slug = AutoSlugField(populate_from='title', verbose_name='URL')

    def get_absolute_url(self):
        return reverse_lazy('tank:game', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'уровень'
        verbose_name_plural = 'уровни'
        ordering = 'difficult', 'title'

    def __str__(self):
        return self.title

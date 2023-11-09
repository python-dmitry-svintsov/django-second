# Generated by Django 4.2.5 on 2023-10-19 14:32

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lapi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='наименование')),
                ('difficult', models.IntegerField(verbose_name='сложность')),
                ('max_enemys', models.IntegerField(verbose_name='макс. кол. врагов')),
                ('speed', models.IntegerField(verbose_name='скорость спауна врагов')),
                ('map', models.FileField(upload_to='lapi', verbose_name='уровень')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', verbose_name='URL')),
            ],
            options={
                'verbose_name': 'уровень',
                'verbose_name_plural': 'уровни',
                'ordering': ['title'],
            },
        ),
    ]
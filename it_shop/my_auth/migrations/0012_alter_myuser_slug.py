# Generated by Django 4.2.5 on 2023-09-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0011_alter_myuser_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='slug',
            field=models.SlugField(max_length=25, unique=True, verbose_name='URL'),
        ),
    ]

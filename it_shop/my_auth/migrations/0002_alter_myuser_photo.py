# Generated by Django 4.2.5 on 2023-09-23 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='photo',
            field=models.ImageField(upload_to='profile/users'),
        ),
    ]

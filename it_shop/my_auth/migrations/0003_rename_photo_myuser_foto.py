# Generated by Django 4.2.5 on 2023-09-23 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0002_alter_myuser_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='photo',
            new_name='foto',
        ),
    ]
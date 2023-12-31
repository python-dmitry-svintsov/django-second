# Generated by Django 4.2.5 on 2023-09-23 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0005_alter_myuser_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='city',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='foto',
            field=models.ImageField(blank=True, upload_to='profile/users'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='sex',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='my_auth.sex'),
        ),
    ]

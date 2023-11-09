# Generated by Django 4.2.5 on 2023-10-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lapi',
            name='background',
            field=models.ImageField(blank=True, null=True, upload_to='lapi/backgrounds/', verbose_name='фон'),
        ),
        migrations.AddField(
            model_name='lapi',
            name='style',
            field=models.IntegerField(blank=True, null=True, verbose_name='style'),
        ),
        migrations.AlterField(
            model_name='lapi',
            name='map',
            field=models.FileField(upload_to='lapi/levels/', verbose_name='уровень'),
        ),
    ]

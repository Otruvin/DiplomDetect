# Generated by Django 3.0.6 on 2020-05-21 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authmanage', '0011_auto_20200519_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='background',
            field=models.ImageField(blank=True, upload_to='', verbose_name='фон'),
        ),
    ]

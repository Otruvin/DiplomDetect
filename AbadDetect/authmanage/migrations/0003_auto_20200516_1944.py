# Generated by Django 3.0.6 on 2020-05-16 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authmanage', '0002_auto_20200516_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='detectedobj',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='owner',
        ),
    ]

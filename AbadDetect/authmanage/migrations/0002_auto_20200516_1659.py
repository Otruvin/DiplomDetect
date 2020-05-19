# Generated by Django 3.0.6 on 2020-05-16 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authmanage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='video_stream',
        ),
        migrations.AlterField(
            model_name='camera',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to=settings.AUTH_USER_MODEL),
        ),
    ]

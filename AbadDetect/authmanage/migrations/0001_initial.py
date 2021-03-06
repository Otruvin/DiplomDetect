# Generated by Django 3.0.6 on 2020-05-12 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=200, verbose_name='Название типа пользователя')),
                ('coast_month', models.DecimalField(decimal_places=3, max_digits=7, verbose_name='Месячная оплата')),
                ('max_count_detected', models.IntegerField(verbose_name='Максимальное количество сохраненных сумок')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_paiment_date', models.DateTimeField(verbose_name='Дата последнего платежа')),
                ('type_cooperator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authmanage.TypeUser')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetectedObj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_detect', models.DateTimeField(auto_now_add=True, verbose_name='Дата обнаружения')),
                ('link_to_image', models.CharField(max_length=300, verbose_name='Ссылка на изображение')),
                ('coord_x', models.IntegerField(verbose_name='Координата по оси Х')),
                ('coord_y', models.IntegerField(verbose_name='Координата по оси У')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detctedB', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_stream', models.IntegerField(default='0', verbose_name='Видеопоток')),
                ('min_area', models.IntegerField(default=0.0, verbose_name='Минимальная площадь')),
                ('max_area', models.IntegerField(default=0.0, verbose_name='Максимальная площадь')),
                ('time_to_detected', models.IntegerField(default=100, verbose_name='Время до обнаружения')),
                ('time_to_warn', models.IntegerField(default=200, verbose_name='Время до сигнала о брошенной сумке')),
                ('time_to_forget', models.IntegerField(default=150, verbose_name='Время до забывания')),
                ('biggest_size', models.DecimalField(decimal_places=3, default=0.0, max_digits=7, verbose_name='Минимальный размер человека')),
                ('distance_to_undetect', models.DecimalField(decimal_places=3, default=200.0, max_digits=7, verbose_name='Максимальное расстояние от не брошенной сумки')),
                ('name_camera', models.CharField(max_length=300, unique=True, verbose_name='Наименование камеры')),
                ('url_camera', models.CharField(max_length=400, verbose_name='url камеры')),
                ('url_background', models.CharField(max_length=400, verbose_name='url фона')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

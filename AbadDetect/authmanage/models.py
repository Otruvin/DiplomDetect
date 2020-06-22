from django.db import models
from django.contrib.auth.models import User

class TypeUser(models.Model):
	type_name = models.CharField('Название типа пользователя', max_length = 200)
	coast_month = models.DecimalField('Месячная оплата', max_digits = 7, decimal_places = 3)
	max_count_detected = models.IntegerField('Максимальное количество сохраненных сумок')

	def __str__(self):
		return "Тип пользователя: " + self.type_name + "; Месячная оплата: " + str(self.coast_month) + \
		"; Максимальное количество сохраненных сумок: " + str(self.max_count_detected)

class Profile(models.Model):
	type_cooperator = models.ForeignKey(TypeUser, on_delete = models.CASCADE)
	last_paiment_date = models.DateTimeField('Дата последнего платежа')
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class DetectedObj(models.Model):
	user = models.ForeignKey(User, related_name="detctedB", on_delete = models.CASCADE)
	date_detect = models.DateTimeField('Дата обнаружения', auto_now_add = True)
	image = models.CharField('изображение', blank=True, null=True, max_length=500)
	coord_x = models.IntegerField('Координата по оси Х')
	coord_y = models.IntegerField('Координата по оси У')

	def __str__(self):
		return "Дата обнаружения: " + str(self.date_detect)

class Camera(models.Model):
	user = models.ForeignKey(User, related_name="cameras",on_delete = models.CASCADE)
	min_area = models.IntegerField('Минимальная площадь', default = 0.0)
	max_area = models.IntegerField('Максимальная площадь', default = 0.0)
	time_to_detected = models.IntegerField('Время до обнаружения', default = 100)
	time_to_warn = models.IntegerField('Время до сигнала о брошенной сумке', default = 200)
	time_to_forget = models.IntegerField('Время до забывания', default = 150)
	biggest_size = models.IntegerField('Минимальный размер человека', default = 0.0)
	distance_to_undetect = models.DecimalField('Максимальное расстояние от не брошенной сумки', max_digits = 11, decimal_places = 3, default = 200.0)
	name_camera = models.CharField('Наименование камеры', max_length = 300, unique = True)
	url_camera = models.CharField('url камеры', max_length = 400)
	background = models.CharField('фон', blank=True, null=True, max_length=500)
	local_connect = models.BooleanField('Локальное соединение', default=True)

	def __str__(self):
		return "Настройки для пользователя " + str(self.user)
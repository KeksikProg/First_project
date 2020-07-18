from django.db import models
from .utilities import get_timestamp_path
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification



#user_registrated = Signal(providing_args = ['instance'])  Тут мы из всех сигналов берем определенный и далее его обрабатываем
#def user_registrated_dispatcher(sender, **kwargs):
#	send_activation_notification(kwags['instance'])
#user_registrated.connect(user_registrated_dispatcher)



class Post(models.Model):
	title = models.CharField(
		max_length = 100,
		verbose_name = 'Название')
	content = models.TextField(
		max_length = 500,
		verbose_name = 'Текст')
	created_at = models.DateTimeField(
		auto_now_add = True,
		db_index = True,
		verbose_name = 'Опубликованно')
	image = models.ImageField(
		blank = True,
		upload_to = get_timestamp_path,
		verbose_name = 'Фотография')
	author = models.ForeignKey(User,
		on_delete = models.CASCADE,
		verbose_name = 'Автор поста')

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		for ai in self.additionalimage_set.all():
			ai.delete()
		super().delete(*args, **kwargs)

	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
		ordering = ['-created_at']

class AdditionalImage(models.Model):
	post = models.ForeignKey(Post,
		on_delete = models.CASCADE,
		verbose_name = 'Пост',)
	
	image = models.ImageField(
		upload_to = get_timestamp_path,
		verbose_name = 'Фотография')

	class Meta:
		verbose_name = 'Фотография'
		verbose_name_plural = 'Фотографии'

class Comment(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete = models.CASCADE,
		verbose_name = 'Пост')
	author = models.CharField(
		max_length = 30,
		verbose_name = 'Автор')
	content = models.TextField(
		verbose_name = 'Содержание')
	created_at = models.DateTimeField(
		auto_now_add = True,
		db_index = True,
		verbose_name = 'Добавлено')

	class Meta:
		verbose_name_plural = 'Комментарии'
		verbose_name = 'Комментарий'
		ordering = ['-created_at']

# Create your models here.

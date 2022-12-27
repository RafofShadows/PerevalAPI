from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(models.Model):
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    name = models.CharField(verbose_name='Имя', max_length=100)
    fam = models.CharField(verbose_name='Фамилия', max_length=100)
    otc = models.CharField(verbose_name='Отчество', max_length=100, blank=True)
    phone = PhoneNumberField(verbose_name='Телефон', null=False, blank=False, unique=True)


class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта', default=0.0)
    longitude = models.FloatField(verbose_name='Долгота', default=0.0)
    height = models.IntegerField(verbose_name='Высота', default=0)


class Images(models.Model):
    date_added = models.DateTimeField(verbose_name='Дата добавления')
    img = models.ImageField(verbose_name='Изображение')


class Areas(models.Model):
    parent = models.IntegerField(default=0)
    title = models.CharField(verbose_name='Наименование', max_length=255)


class PassData(models.Model):
    class Meta:
        db_table = 'pereval_added'

    beauty_title = models.CharField(max_length=100)
    title = models.CharField('Название', max_length=255)
    other_titles = models.CharField(verbose_name='Альтернативное название', max_length=255, blank=True)
    connect = models.TextField(verbose_name='Что соединяет', blank=True)
    add_time = models.DateTimeField(verbose_name='Дата добавления')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level_winter = models.CharField()
    image = models.ManyToManyField(Images, through='PerevalImages')


class PerevalImages(models.Model):
    pereval = models.ForeignKey(PassData, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE())





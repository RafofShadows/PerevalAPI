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


class Image(models.Model):
    class Meta:
        db_table = 'pereval_images'

    date_added = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    img = models.BinaryField(verbose_name='Изображение')
    title = models.CharField(verbose_name='Название', max_length=150)


class Area(models.Model):
    class Meta:
        db_table = 'pereval_areas'

    parent = models.IntegerField(default=0)
    title = models.CharField(verbose_name='Наименование', max_length=255, unique=True)


class Level(models.Model):
    LEVELS = [
        ('1А', '1А'),
        ('1Б', '1Б'),
        ('2А', '2А'),
        ('2Б', '2Б'),
        ('3А', '3А'),
        ('3Б', '3Б'),
    ]

    winter = models.CharField(verbose_name='Категория трудности зимой', max_length=2, choices=LEVELS, default=LEVELS[0], blank=True)
    spring = models.CharField(verbose_name='Категория трудности весной', max_length=2, choices=LEVELS, default=LEVELS[0], blank=True)
    summer = models.CharField(verbose_name='Категория трудности летом', max_length=2, choices=LEVELS, default=LEVELS[0], blank=True)
    autumn = models.CharField(verbose_name='Категория трудности осенью', max_length=2, choices=LEVELS, default=LEVELS[0], blank=True)


class PassData(models.Model):
    class Meta:
        db_table = 'pereval_added'

    beauty_title = models.CharField(max_length=100)
    title = models.CharField('Название', max_length=255)
    other_titles = models.CharField(verbose_name='Альтернативное название', max_length=255, blank=True)
    area = models.ForeignKey(Area, verbose_name='Горный хребет', blank=True, null=True, on_delete=models.SET_NULL)
    add_time = models.DateTimeField(verbose_name='Дата добавления')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, verbose_name='Координаты', on_delete=models.CASCADE)
    levels = models.ForeignKey(Level, verbose_name='Категория трудности', on_delete=models.CASCADE)

    STATUSES = [
        ('new', 'Новый'),
        ('pending', 'В работе'),
        ('accepted', 'информация принята'),
        ('rejected', 'информация не принята'),
    ]
    status = models.CharField(verbose_name='Статус модерации', max_length=100, choices=STATUSES, default='new')
    image = models.ManyToManyField(Image, through='PerevalImages')


class PerevalImages(models.Model):
    pereval = models.ForeignKey(PassData, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Activities(models.Model):
    class Meta:
        db_table = 'spr_activities_types'

    title = models.CharField(verbose_name='Способ передвижения', max_length=100)





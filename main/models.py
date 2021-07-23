from django.db import models
from django.dispatch import Signal
from django.contrib.auth.models import AbstractUser

from .utilities import set_hours, send_activation_notification, get_timestamp_path


class Bid(models.Model):
    STATUS = (('a', 'Заявка(актив)'), ('b', 'Заявка(откл.)'), ('c', 'Заявка обработана'))
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.CharField('Электронная почта', max_length=50)
    status = models.CharField('Статус', max_length=1, choices=STATUS)
    description = models.TextField('Характеристика')

    class Meta:
        verbose_name = 'Член организации'
        verbose_name_plural = 'Члены организации'

    def __str__(self):
        return f'{self.first_name} + {self.last_name}'


class Event(models.Model):
    name = models.CharField('Название', max_length=200)
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    description = models.TextField('Описание', null=True, blank=True)
    volunteers = models.ManyToManyField('Volunteer', verbose_name='Волонтёры', blank=True)
    date = models.DateTimeField('Дата')
    hours = models.FloatField('Часы', max_length=24)
    is_over = models.BooleanField('Завершено')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ('-date',)

    def get_volunteers(self):
        return ", ".join([str(p) for p in self.volunteers.all()])
    get_volunteers.short_description = 'Волонтёры'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_over:
            set_hours(self)
        super().save(*args, **kwargs)


class Volunteer(AbstractUser):
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    hours = models.FloatField('Часы', max_length=24, default=0)
    status = models.BooleanField('Статус', default=0)
    description = models.TextField('Характеристика')

    class Meta:
        verbose_name = 'Волонтёр'
        verbose_name_plural = 'Волонтёры'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)

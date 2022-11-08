from django.contrib.auth.models import User
from django.core import validators
from django.db import models


class Device(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255,
        db_index=True,
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE,
        verbose_name='Устройство',
    )
    ratio = models.FloatField(
        verbose_name='Коэффициент',
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(1),
        ]
    )
    min_value = models.SmallIntegerField(
        verbose_name='Нижняя граница значения',
        default=-100,
    )
    max_value = models.SmallIntegerField(
        verbose_name='Верхняя граница значения',
        default=100,
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name} - {self.device.name}'


class TagValue(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        verbose_name='Тег',
    )
    value = models.FloatField(
        verbose_name='Значение',
    )
    version = models.CharField(
        verbose_name='version',
        max_length=255,
        blank=True, default='',
    )
    timestamp = models.DateTimeField(
        verbose_name='timestamp',
    )

    class Meta:
        verbose_name = 'Значение тега'
        verbose_name_plural = 'Значения тегов'

    def __str__(self):
        return str(self.id)

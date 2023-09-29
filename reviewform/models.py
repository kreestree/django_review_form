from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe

from io import BytesIO
from PIL import Image as PilImage
from django.core.files import File

from django.utils import timezone


# Create your models here.
class FactoryNumber(models.Model):
    factory_number = models.IntegerField(verbose_name='Заводской номер',
                                         unique=True,
                                         default=260_000,
                                         validators=[MinValueValidator(260_000), MaxValueValidator(261_000)])

    def __str__(self):
        return str(self.factory_number)

    class Meta:
        verbose_name = 'Заводской номер'
        verbose_name_plural = 'Заводские номера'
        ordering = ['factory_number']


class FactoryArea(models.Model):
    factory_area = models.CharField(max_length=150, verbose_name='Участок')

    def __str__(self):
        return str(self.factory_area)

    class Meta:
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'
        ordering = ['factory_area']


class Problems(models.Model):
    factory_number = models.ForeignKey('FactoryNumber', on_delete=models.CASCADE, verbose_name='Заводской номер')
    factory_area = models.ForeignKey('FactoryArea', on_delete=models.CASCADE, verbose_name='Участок')
    problem = models.TextField(max_length=2000, verbose_name='Проблема')
    employee_full_name = models.CharField(max_length=150, verbose_name='Ф.И.О. работника')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return (f'Проблема на {self.factory_area} '
                f'з.з. {self.factory_number} '
                f'от {self.time_create.strftime("%d.%m.%Y %H:%M %Z")}')

    class Meta:
        verbose_name = 'Проблема'
        verbose_name_plural = 'Проблемы'


class Image(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE, related_name='Проблема', verbose_name='Проблема')
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Фото')

    @staticmethod
    def compress(image):
        im = PilImage.open(image)
        im = im.convert('RGB')
        im_io = BytesIO()  # create a BytesIO object
        im.save(im_io, 'JPEG', quality=90, optimize=True)  # save image to BytesIO object
        new_image = File(im_io, name=image.name)  # create a django-friendly Files object
        return new_image

    def save(self, *args, **kwargs):
        new_image = self.compress(self.image)  # call the compress function
        self.image = new_image  # set self.image to new_image
        super().save(*args, **kwargs)  # save

    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}" target="_blank">'
                             f'<img src="{self.image.url}" width=auto height="200" />'
                             f'</a>')
        return ""

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

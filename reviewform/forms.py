from django import forms
from django.core.exceptions import ValidationError

from .models import *


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            images = [single_file_clean(d, initial) for d in data]
        else:
            images = single_file_clean(data, initial)

        if len(images) > 10:
            raise ValidationError('Максимум 10 изображений')
        for image in images:
            if image.content_type.split('/')[0] != 'image':
                raise ValidationError('Допускаются только изображения')
            elif image.size > 5_242_880:
                raise ValidationError('Изображение не должно весить больше 5 МБ')
        return images


class AddProblemForm(forms.ModelForm):
    image_field = MultipleImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['problem'].label = 'Опишите проблему'
        self.fields['employee_full_name'].label = 'Ваше имя'
        self.fields['image_field'].label = 'Прикрепите изображения (не более десяти)'
        self.fields['image_field'].widget.attrs.update({'accept': "image/*"})

        for field in 'factory_number', 'factory_area':
            self.fields[field].empty_label = 'Не выбран'
            self.fields[field].widget.attrs['class'] = 'form-select'

        for field in 'problem', 'employee_full_name':
            self.fields[field].widget.attrs.update({'placeholder': self.fields[field].label})

        for field in 'problem', 'employee_full_name', 'image_field':
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Problems
        fields = ['factory_number', 'factory_area', 'problem', 'employee_full_name']

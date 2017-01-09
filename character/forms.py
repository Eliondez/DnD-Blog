from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):

    photo = forms.FileField(label='Маленькое фото', required=False)
    photo_full = forms.FileField(label='Большое фото', required=False)
    class Meta:
        model = Character
        fields = [
            'name',
            'char_class',
            'description',
            'public_stats',
            'private_stats',
            'photo',
            'photo_full',
        ]
        labels = {
            'name': 'Имя персонажа',
            'char_class': 'Класс персонажа',
            'description': 'Описание',
            'public_stats': 'Открытые характеристики',
            'private_stats': 'Скрытые характеристики',
        }
        widgets = {
            'photo': forms.FileInput(),
        }

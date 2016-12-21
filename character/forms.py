from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    name = forms.CharField(label='Имя персонажа', widget=forms.TextInput(attrs={'class': 'form-control'}))
    char_class = forms.CharField(label='Класс персонажа', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))
    photo = forms.FileField(label='Маленькое фото', required=False)
    photo_full = forms.FileField(label='Большое фото', required=False)
    class Meta:
        model = Character
        fields = [
            'name',
            'char_class',
            'description',
            'photo',
            'photo_full',
        ]

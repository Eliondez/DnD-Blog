from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            # print('Проверяем юзверя', username, password)
            if not user:
                raise forms.ValidationError('Что-то пошло не так. Засните и проснитесь заново')
            if not user.is_active:
                raise forms.ValidationError('Пользователь заблокирован')
        return super(UserLoginForm, self).clean()

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Почтовый адрес', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Пароль ещё раз', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

    def clean_password2(self):
        pw = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw != pw2:
            raise forms.ValidationError('Пароли должны совпадать')
        return pw
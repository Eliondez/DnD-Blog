from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            # print('Проверяем юзверя', username, password)
            if not user:
                raise forms.ValidationError('Логин или пароль не подходят.')
            if not user.is_active:
                raise forms.ValidationError('Пользователь заблокирован')
        return super(UserLoginForm, self).clean()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Пароль ещё раз', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
        labels = {
            'username': 'Имя пользователя',
            'email': 'Почтовый адрес',
        }

    def clean_password2(self):
        pw = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw != pw2:
            raise forms.ValidationError('Пароли должны совпадать')
        return pw
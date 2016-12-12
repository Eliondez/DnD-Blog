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
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Нет такого юзверя')
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
            if not user.is_active:
                raise forms.ValidationError('Пользователь заблокирован')
        return super(UserLoginForm, self).clean()

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя')
    email = forms.EmailField(label='Почтовый адрес')
    email2 = forms.EmailField(label='Почтовый адрес ещё раз')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = {
            'username',
            'email',
            'email2',
            'password'
        }

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('Emails must match')
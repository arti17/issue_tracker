from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=100, label='Логин', required=True)
    password = forms.CharField(max_length=100, label='Пароль', required=True,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, label='Подтверждение пароля', required=True,
                                       widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, required=False, label='Имя')
    last_name = forms.CharField(max_length=100, required=False, label='Фамилия')
    email = forms.EmailField(required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('Такой пользователь уже существует',
                                  code='user_exists')
        except User.DoesNotExist:
            return username

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if password_1 != password_2:
            raise ValidationError('Пароли не совпадают',
                                  code='passwords_do_not_match')
        elif not first_name and not last_name:
            raise ValidationError('Имя или Фамилия должны быть заполнены',
                                  code='first_name and last_name_exists')

        return self.cleaned_data


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label='Новый пароль', strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвержение пароля', strip=False, widget=forms.PasswordInput)
    old_password = forms.CharField(label='Старый пароль', strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError('Пароли не совпадают')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise ValidationError('Неверный старый пароль')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']

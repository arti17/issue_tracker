from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pict', verbose_name='Аватар')
    about_user = models.TextField(max_length=500, null=True, blank=True, verbose_name='О себе')
    link_to_github = models.URLField(max_length=100, null=True, blank=True, verbose_name='Ссылка на github')

    def __str__(self):
        return self.user.get_full_name() + 'профиль'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

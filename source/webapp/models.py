from django.db import models


class Issue(models.Model):
    summary = models.CharField(max_length=60, verbose_name='Краткое описание')
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name='Полное описание')
    status = models.ForeignKey('webapp.Status', related_name='issues', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('webapp.Type', related_name='issues', on_delete=models.PROTECT, verbose_name='Тип')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Status(models.Model):
    name = models.CharField(max_length=20, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'


class Type(models.Model):
    name = models.CharField(max_length=20, verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'

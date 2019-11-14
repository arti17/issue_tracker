from django.contrib.auth.models import User
from django.db import models

PROJECT_STATUS_ACTIVE = 'active'
PROJECT_STATUS_BLOCKED = 'blocked'
PROJECT_STATUS_CHOICES = (
    (PROJECT_STATUS_ACTIVE, 'Активен'),
    (PROJECT_STATUS_BLOCKED, 'Заблокирован')
)


class Issue(models.Model):
    summary = models.CharField(max_length=60, verbose_name='Краткое описание')
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name='Полное описание')
    status = models.ForeignKey('webapp.Status', related_name='issues', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('webapp.Type', related_name='issues', on_delete=models.PROTECT, verbose_name='Тип')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    project = models.ForeignKey('webapp.Project', related_name='issues', on_delete=models.PROTECT, verbose_name='Проект')
    created_by = models.ForeignKey(User, related_name='created_issues', on_delete=models.PROTECT, verbose_name='Создатель')
    assigned_to = models.ForeignKey(User, related_name='assigned_issues', on_delete=models.PROTECT, verbose_name='Исполнитель')

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        permissions = [
            ('can_add_issue_for_project', 'Может добавлять задачи к проекту')
        ]


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


class Project(models.Model):
    summary = models.CharField(max_length=60, verbose_name='Название')
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name='Описание')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default=PROJECT_STATUS_ACTIVE, verbose_name='Статус')

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Team(models.Model):
    user = models.ForeignKey(User, related_name='teams', on_delete=models.PROTECT, verbose_name='Пользователь')
    project = models.ForeignKey('webapp.Project', related_name='teams', on_delete=models.PROTECT, verbose_name='Проект')
    start_date = models.DateField(null=True, blank=True, verbose_name='Дата начала работы ')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания работы')

    def __str__(self):
        return f'{self.user.username} - {self.project.summary}'

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

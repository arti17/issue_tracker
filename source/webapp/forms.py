from django import forms
from django.forms import widgets
from webapp.models import Issue, Status, Type


class IssueForm(forms.Form):
    summary = forms.CharField(max_length=60, required=True, label='Краткое описание')
    description = forms.CharField(max_length=400, required=False, label='Полное описание', widget=widgets.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус задачи',
                                    empty_label='Выберите статус задачи')
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, label='Тип задачи',
                                  empty_label='Выберите тип задачи')


class StatusForm(forms.Form):
    name = forms.CharField(max_length=20, required=True, label='Статус')


class TypeForm(forms.Form):
    name = forms.CharField(max_length=20, required=True, label='Тип задачи')

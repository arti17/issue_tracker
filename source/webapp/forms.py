from django import forms
from django.contrib.auth.models import User

from webapp.models import Issue, Status, Type, Project


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ['create_date', 'created_by']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['summary', 'description']


class IssueProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.projects = kwargs.pop('projects')
        print(self.projects)
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(teams__project__in=self.projects)

    class Meta:
        model = Issue
        exclude = ['create_date', 'project', 'created_by']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=60, required=False, label='Поиск')

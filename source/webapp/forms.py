from django import forms
from webapp.models import Issue, Status, Type, Project


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ['create_date']


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
    class Meta:
        model = Issue
        exclude = ['create_date', 'project']

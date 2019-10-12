from django import forms
from webapp.models import Issue, Status, Type, Project


class IssueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all().filter(status__icontains='active')

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


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=60, required=False, label='Поиск')

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from webapp.models import Issue, PROJECT_STATUS_BLOCKED
from webapp.forms import IssueForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .base_views import DetailView


class IndexView(ListView):
    template_name = 'issue/index.html'
    context_object_name = 'issues'
    model = Issue
    ordering = '-create_date'
    paginate_by = 5


class IssueView(DetailView):
    template_name = 'issue/issue_detail.html'
    model = Issue
    context_key = 'issue'


class IssueCreateView(CreateView):
    template_name = 'issue/create_issue.html'
    model = Issue
    form_class = IssueForm

    def get_success_url(self):
        return reverse('index')


class IssueUpdateView(UpdateView):
    model = Issue
    class_form = IssueForm
    template_name = 'issue/update_issue.html'
    context_object_name = 'issue'
    success_url = '/'
    fields = ['summary', 'description', 'status', 'type', 'project']

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.project.status == PROJECT_STATUS_BLOCKED:
            raise Http404
        return render(request, 'issue/update_issue.html', {'form': self.class_form(instance=issue), self.context_object_name: issue})

    def get_object(self):
        issue_pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=issue_pk)


class IssueDeleteView(DeleteView):
    model = Issue
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.project.status == PROJECT_STATUS_BLOCKED:
            raise Http404
        return render(request, 'issue/delete_issue.html', {'issue': issue})

    def get_object(self):
        issue_pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=issue_pk)




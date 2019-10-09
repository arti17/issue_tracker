from django.urls import reverse, reverse_lazy
from webapp.models import Issue
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


class IssueDeleteView(DeleteView):
    model = Issue
    template_name = 'issue/delete_issue.html'
    context_object_name = 'issue'
    success_url = reverse_lazy('index')

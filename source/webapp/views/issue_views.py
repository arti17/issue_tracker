from django.urls import reverse
from webapp.models import Issue
from webapp.forms import IssueForm
from django.views.generic import ListView, CreateView, UpdateView
from .base_views import DetailView, DeleteView


class IndexView(ListView):
    template_name = 'issue/index.html'
    context_object_name = 'issues'
    model = Issue
    ordering = '-create_date'
    paginate_by = 2
    paginate_orphans = 0


class IssueView(DetailView):
    template_name = 'issue/detail.html'
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
    fields = ['summary', 'description', 'status', 'type']


class IssueDeleteView(DeleteView):
    model = Issue
    confirm_template_name = 'issue/delete_issue.html'
    context_object_name = 'issue'
    success_url = '/'
    confirm_of_delete = True

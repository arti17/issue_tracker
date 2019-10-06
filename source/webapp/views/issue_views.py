from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from webapp.models import Issue
from webapp.forms import IssueForm
from django.views.generic import View, ListView, CreateView
from .base_views import DetailView, UpdateView


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
    context_key = 'issue'


class IssueDeleteView(View):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        return render(request, 'issue/delete_issue.html', {'issue': issue})

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return redirect('index')

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from webapp.models import Issue
from webapp.forms import IssueForm
from django.views.generic import View, ListView, CreateView
from .base_views import DetailView


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


class IssueUpdateView(View):
    def get(self, request, *args, **kwargs):
        issue_pk = kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=issue_pk)
        form = IssueForm(data={
            'summary': issue.summary,
            'description': issue.description,
            'status': issue.status.id,
            'type': issue.type.id
        })
        return render(request, 'issue/update_issue.html', {'form': form, 'issue': issue})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        issue_pk = kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=issue_pk)
        if form.is_valid():
            issue.summary = form.cleaned_data['summary']
            issue.description = form.cleaned_data['description']
            issue.status = form.cleaned_data['status']
            issue.type = form.cleaned_data['type']
            issue.save()
            return redirect('index')
        else:
            return render(request, 'issue/update_issue.html', {'form': form, 'issue': issue})


class IssueDeleteView(View):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        return render(request, 'issue/delete_issue.html', {'issue': issue})

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return redirect('index')

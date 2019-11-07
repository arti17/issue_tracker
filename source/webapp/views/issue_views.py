from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode

from webapp.models import Issue, PROJECT_STATUS_BLOCKED, Team, Project
from webapp.forms import IssueForm, SimpleSearchForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .base_views import DetailView


class IndexView(ListView):
    template_name = 'issue/index.html'
    context_object_name = 'issues'
    model = Issue
    ordering = ['-create_date']
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class IssueView(DetailView):
    template_name = 'issue/issue_detail.html'
    model = Issue
    context_key = 'issue'


class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = 'issue/create_issue.html'
    model = Issue
    form_class = IssueForm

    def get_form(self, form_class=None):
        form = super().get_form()
        username = self.request.user
        teams = Team.objects.filter(user__username__icontains=username)
        user_projects = []
        for team in teams:
            user_projects.append(team.project)
        form.fields['project'].queryset = Project.objects.filter(summary__in=user_projects).filter(status='active')
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:index')


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    class_form = IssueForm
    template_name = 'issue/update_issue.html'
    context_object_name = 'issue'
    fields = ['summary', 'description', 'status', 'type', 'project', 'assigned_to']

    def test_func(self):
        issue = self.get_object()
        project = issue.project
        teams = Team.objects.filter(project=project)
        users_id = []
        for team in teams:
            users_id.append(team.user.pk)
        return self.request.user.pk in users_id

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.project.status == PROJECT_STATUS_BLOCKED:
            raise Http404
        return render(request, 'issue/update_issue.html', {'form': self.class_form(instance=issue), self.context_object_name: issue})

    def get_object(self):
        issue_pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=issue_pk)

    def get_success_url(self):
        return reverse('webapp:index')


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = reverse_lazy('webapp:index')

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.project.status == PROJECT_STATUS_BLOCKED:
            raise Http404
        return render(request, 'issue/delete_issue.html', {'issue': issue})

    def test_func(self):
        issue = self.get_object()
        project = issue.project
        teams = Team.objects.filter(project=project)
        users_id = []
        for team in teams:
            users_id.append(team.user.pk)
        return self.request.user.pk in users_id

    def get_object(self):
        issue_pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=issue_pk)




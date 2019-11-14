from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import View

from webapp.forms import ProjectForm, IssueProjectForm, SimpleSearchForm, AddProjectUsersForm
from webapp.models import Project, PROJECT_STATUS_BLOCKED, PROJECT_STATUS_ACTIVE, Team, Issue


class ProjectView(ListView):
    template_name = 'project/project_list.html'
    model = Project

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        if self.search_value:
            context['active_projects'] = Project.objects.filter(summary__icontains=self.search_value, status=PROJECT_STATUS_ACTIVE).order_by('create_date')
            context['blocked_projects'] = Project.objects.filter(summary__icontains=self.search_value, status=PROJECT_STATUS_BLOCKED).order_by('create_date')
        else:
            context['active_projects'] = Project.objects.filter(status=PROJECT_STATUS_ACTIVE).order_by('create_date')
            context['blocked_projects'] = Project.objects.filter(status=PROJECT_STATUS_BLOCKED).order_by('create_date')
        return context

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectDetailView(DetailView):
    template_name = 'project/project_detail.html'
    model = Project
    context_key = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = context['project'].issues.order_by('-create_date')
        project_pk = self.kwargs.get('pk')
        teams = Team.objects.filter(project=project_pk, end_date=None)
        context['teams'] = teams
        return context


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project/create_project.html'
    model = Project
    form_class = ProjectForm
    permission_required = 'webapp.add_project'
    permission_denied_message = "Доступ запрещён"

    def form_valid(self, form):
        self.object = form.save()
        users = form.cleaned_data['users']
        date = datetime.now()
        self.add_created_user()
        for user in users:
            Team.objects.create(user=user, project=self.object, start_date=date)
        return redirect(self.get_success_url())

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['users'].queryset = User.objects.all().exclude(username=self.request.user)
        return form

    def add_created_user(self):
        user = self.request.user
        project = self.object
        date = datetime.now()
        Team.objects.create(user=user, project=project, start_date=date)

    def get_success_url(self):
        return reverse('webapp:projects_list')


class ProjectCreateIssueView(UserPassesTestMixin, PermissionRequiredMixin, CreateView):
    template_name = 'issue/create_issue.html'
    form_class = IssueProjectForm
    permission_required = 'webapp.change_issue'
    permission_denied_message = "Доступ запрещён"

    def test_func(self):
        project_pk = self.kwargs.get('pk')
        project = Project.objects.get(pk=project_pk)
        teams = Team.objects.filter(project=project.pk)
        users_id = []
        for team in teams:
            users_id.append(team.user.pk)
        return self.request.user.pk in users_id

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        project.issues.create(created_by=self.request.user, **form.cleaned_data)
        return redirect('webapp:project_detail', pk=project_pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_pk = self.kwargs.get('pk')
        project = Project.objects.filter(pk=project_pk)
        kwargs['projects'] = project
        return kwargs


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = 'webapp.delete_project'
    permission_denied_message = "Доступ запрещён"

    def get(self, request, *args, **kwargs):
        project_pk = kwargs.get('pk')
        project = Project.objects.get(pk=project_pk)
        project.status = PROJECT_STATUS_BLOCKED
        project.save()
        return redirect('webapp:projects_list')

    def get_success_url(self):
        return reverse('webapp:projects_list')


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    class_form = ProjectForm
    template_name = 'project/update_project.html'
    context_object_name = 'project'
    fields = ['summary', 'description']
    permission_required = 'webapp.change_project'
    permission_denied_message = "Доступ запрещён"

    def get_success_url(self):
        return reverse('webapp:projects_list')


class AddProjectUsers(PermissionRequiredMixin, CreateView):
    template_name = 'project/add_project_users.html'
    model = Team
    form_class = AddProjectUsersForm
    permission_required = 'webapp.can_add_issue_for_project'
    permission_denied_message = "Доступ запрещён"

    def form_valid(self, form):
        users = form.cleaned_data['users']
        project = self.get_project()
        date = datetime.now()
        for user in users:
            Team.objects.create(user=user, project=project, start_date=date)
        return redirect('webapp:project_detail', project.pk)

    def get_form(self, form_class=None):
        form = super().get_form()
        project = self.get_project()
        teams = Team.objects.filter(project=project.pk)
        users = []
        for team in teams:
            if team.end_date:
                continue
            users.append(team.user)
        form.fields['users'].queryset = User.objects.all().exclude(username__in=users)
        return form

    def get_success_url(self):
        return reverse('webapp:project_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project.objects.filter(pk=pk))
        context['project'] = project
        return context

    def get_project(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=pk)


class DeleteProjectUser(PermissionRequiredMixin, View):
    permission_required = 'webapp.delete_team'
    permission_denied_message = "Доступ запрещён"

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        user_id = request.POST.get('user')
        team = Team.objects.get(project=project_id, user=int(user_id), end_date__isnull=True)
        date = datetime.now()
        team.end_date = date
        team.save()
        return redirect(reverse('webapp:project_detail', kwargs={'pk': project_id}))

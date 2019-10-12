from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from webapp.forms import ProjectForm, IssueProjectForm, SimpleSearchForm
from webapp.models import Project, PROJECT_STATUS_BLOCKED, PROJECT_STATUS_ACTIVE


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
        return context


class ProjectCreateView(CreateView):
    template_name = 'project/create_project.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('projects_list')


class ProjectCreateIssueView(CreateView):
    template_name = 'issue/create_issue.html'
    form_class = IssueProjectForm

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        project.issues.create(**form.cleaned_data)
        return redirect('project_detail', pk=project_pk)


class ProjectDeleteView(DeleteView):
    model = Project

    def post(self, request, *args, **kwargs):
        project_pk = kwargs.get('pk')
        project = Project.objects.get(pk=project_pk)
        project.status = PROJECT_STATUS_BLOCKED
        project.save()
        return redirect('projects_list')

    def get_success_url(self):
        return reverse('projects_list')


class ProjectUpdateView(UpdateView):
    model = Project
    class_form = ProjectForm
    template_name = 'project/update_project.html'
    context_object_name = 'project'
    success_url = '/projects/'
    fields = ['summary', 'description']

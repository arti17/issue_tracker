from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from webapp.forms import ProjectForm, IssueProjectForm
from webapp.models import Project


class ProjectView(ListView):
    template_name = 'project/project_list.html'
    model = Project

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.order_by('create_date')
        return context


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
        try:
            return self.delete(request, *args, **kwargs)
        except BaseException as error:
            return render(request, 'project/project_list.html', {'errors': error})

    def get_success_url(self):
        return reverse('projects_list')


class ProjectUpdateView(UpdateView):
    model = Project
    class_form = ProjectForm
    template_name = 'project/update_project.html'
    context_object_name = 'project'
    success_url = '/projects/'
    fields = ['summary', 'description']
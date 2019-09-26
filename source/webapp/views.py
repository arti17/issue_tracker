from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Issue, Status, Type
from webapp.forms import IssueForm, StatusForm, TypeForm
from django.views.generic import TemplateView, View


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = Issue.objects.all()
        return context


class IssueView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data()
        context['issue'] = get_object_or_404(Issue, pk=pk)
        return context


class IssueCreateView(View):
    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'create_issue.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            Issue.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
                type=form.cleaned_data['type']
            )
            return redirect('index')
        else:
            return render(request, 'create_issue.html', {'form': form})


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
        return render(request, 'update_issue.html', {'form': form, 'issue': issue})

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
            return render(request, 'update_issue.html', {'form': form, 'issue': issue})


class IssueDeleteView(View):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        return render(request, 'delete_issue.html', {'issue': issue})

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return redirect('index')


class StatusView(TemplateView):
    template_name = 'status_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all().order_by('name')
        return context


class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'create_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        if form.is_valid():
            Status.objects.create(name=form.cleaned_data['name'])
            return redirect('statuses_list')
        else:
            return render(request, 'create_status.html', {'form': form})


class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_pk)
        form = StatusForm(data={'name': status.name})
        return render(request, 'update_status.html', {'form': form, 'status': status})

    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        status_pk = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_pk)
        if form.is_valid():
            status.name = form.cleaned_data['name']
            status.save()
            return redirect('statuses_list')
        else:
            return render(request, 'update_status.html', {'form': form, 'status': status})


class StatusDeleteView(View):
    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        try:
            status.delete()
            return redirect('statuses_list')
        except BaseException as error:
            return render(request, 'status_list.html', {'errors': error})


class TypeView(TemplateView):
    template_name = 'types_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all().order_by('name')
        return context


class TypeCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TypeForm()
        return render(request, 'create_type.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TypeForm(data=request.POST)
        if form.is_valid():
            Type.objects.create(name=form.cleaned_data['name'])
            return redirect('types_list')
        else:
            return render(request, 'create_type.html', {'form': form})


class TypeUpdateView(View):
    def get(self, request, *args, **kwargs):
        type_pk = kwargs.get('pk')
        type = get_object_or_404(Type, pk=type_pk)
        form = TypeForm(data={'name': type.name})
        return render(request, 'update_type.html', {'form': form, 'type': type})

    def post(self, request, *args, **kwargs):
        form = TypeForm(data=request.POST)
        type_pk = kwargs.get('pk')
        type = get_object_or_404(Type, pk=type_pk)
        if form.is_valid():
            type.name = form.cleaned_data['name']
            type.save()
            return redirect('types_list')
        else:
            return render(request, 'update_type.html', {'form': form, 'type': type})


class TypeDeleteView(View):
    def post(self, request, pk):
        type = get_object_or_404(Type, pk=pk)
        try:
            type.delete()
            return redirect('types_list')
        except BaseException as error:
            return render(request, 'types_list.html', {'errors': error})

from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Status
from webapp.forms import StatusForm
from django.views.generic import View, ListView


class StatusView(ListView):
    template_name = 'status/status_list.html'
    context_object_name = 'statuses'
    model = Status
    ordering = 'name'


class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'status/create_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        if form.is_valid():
            Status.objects.create(name=form.cleaned_data['name'])
            return redirect('statuses_list')
        else:
            return render(request, 'status/create_status.html', {'form': form})


class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_pk)
        form = StatusForm(data={'name': status.name})
        return render(request, 'status/update_status.html', {'form': form, 'status': status})

    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        status_pk = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_pk)
        if form.is_valid():
            status.name = form.cleaned_data['name']
            status.save()
            return redirect('statuses_list')
        else:
            return render(request, 'status/update_status.html', {'form': form, 'status': status})


class StatusDeleteView(View):
    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        try:
            status.delete()
            return redirect('statuses_list')
        except BaseException as error:
            return render(request, 'status/status_list.html', {'errors': error})

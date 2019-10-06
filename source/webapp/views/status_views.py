from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.models import Status
from webapp.forms import StatusForm
from django.views.generic import View, ListView, CreateView
from .base_views import UpdateView


class StatusView(ListView):
    template_name = 'status/status_list.html'
    context_object_name = 'statuses'
    model = Status
    ordering = 'name'


class StatusCreateView(CreateView):
    template_name = 'status/create_status.html'
    model = Status
    form_class = StatusForm

    def get_success_url(self):
        return reverse('statuses_list')


class StatusUpdateView(UpdateView):
    model = Status
    class_form = StatusForm
    template_name = 'status/update_status.html'
    context_key = 'status'
    success_url = '/statuses/'


class StatusDeleteView(View):
    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        try:
            status.delete()
            return redirect('statuses_list')
        except BaseException as error:
            return render(request, 'status/status_list.html', {'errors': error})

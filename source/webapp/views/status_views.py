from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from webapp.models import Status
from webapp.forms import StatusForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class StatusView(ListView):
    template_name = 'status/status_list.html'
    context_object_name = 'statuses'
    model = Status
    ordering = 'name'


class StatusCreateView(LoginRequiredMixin, CreateView):
    template_name = 'status/create_status.html'
    model = Status
    form_class = StatusForm

    def get_success_url(self):
        return reverse('webapp:statuses_list')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    class_form = StatusForm
    template_name = 'status/update_status.html'
    context_object_name = 'status'
    success_url = '/statuses/'
    fields = ['name']


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status

    def get(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except BaseException as error:
            return render(request, 'status/status_list.html', {'errors': error})

    def get_success_url(self):
        return reverse('webapp:statuses_list')

from django.urls import reverse

from webapp.models import Status
from webapp.forms import StatusForm
from django.views.generic import View, ListView, CreateView
from .base_views import UpdateView, DeleteView


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
    context_object_name = 'status'
    success_url = '/statuses/'


class StatusDeleteView(DeleteView):
    model = Status
    confirm_template_name = 'status/confirm_of_delete_status.html'
    context_object_name = 'status'
    template_name = 'status/status_list.html'
    success_url = '/statuses/'
    confirm_of_delete = True

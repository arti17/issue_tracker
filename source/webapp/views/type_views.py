from django.shortcuts import render
from django.urls import reverse
from webapp.models import Type
from webapp.forms import TypeForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class TypeView(ListView):
    template_name = 'type/types_list.html'
    context_object_name = 'types'
    model = Type
    ordering = 'name'


class TypeCreateView(CreateView):
    template_name = 'type/create_type.html'
    model = Type
    form_class = TypeForm

    def get_success_url(self):
        return reverse('types_list')


class TypeUpdateView(UpdateView):
    model = Type
    class_form = TypeForm
    template_name = 'type/update_type.html'
    context_object_name = 'type'
    success_url = '/types/'
    fields = ['name']


class TypeDeleteView(DeleteView):
    model = Type

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except BaseException as error:
            return render(request, 'type/types_list.html', {'errors': error})

    def get_success_url(self):
        return reverse('types_list')

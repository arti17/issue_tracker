from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from webapp.models import Type
from webapp.forms import TypeForm
from django.views.generic import View, ListView, CreateView
from .base_views import UpdateView


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
    context_key = 'type'
    success_url = '/types/'


class TypeDeleteView(View):
    def post(self, request, pk):
        type = get_object_or_404(Type, pk=pk)
        try:
            type.delete()
            return redirect('types_list')
        except BaseException as error:
            return render(request, 'type/types_list.html', {'errors': error})

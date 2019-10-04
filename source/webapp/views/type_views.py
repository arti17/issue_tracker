from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from webapp.models import Type
from webapp.forms import TypeForm
from django.views.generic import View, ListView, CreateView


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


class TypeUpdateView(View):
    def get(self, request, *args, **kwargs):
        type_pk = kwargs.get('pk')
        type = get_object_or_404(Type, pk=type_pk)
        form = TypeForm(data={'name': type.name})
        return render(request, 'type/update_type.html', {'form': form, 'type': type})

    def post(self, request, *args, **kwargs):
        form = TypeForm(data=request.POST)
        type_pk = kwargs.get('pk')
        type = get_object_or_404(Type, pk=type_pk)
        if form.is_valid():
            type.name = form.cleaned_data['name']
            type.save()
            return redirect('types_list')
        else:
            return render(request, 'type/update_type.html', {'form': form, 'type': type})


class TypeDeleteView(View):
    def post(self, request, pk):
        type = get_object_or_404(Type, pk=pk)
        try:
            type.delete()
            return redirect('types_list')
        except BaseException as error:
            return render(request, 'type/types_list.html', {'errors': error})

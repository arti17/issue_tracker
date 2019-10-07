from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, View


class DetailView(TemplateView):
    context_key = 'objects'
    model = None
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg)
        context = super().get_context_data(**kwargs)
        context[self.context_key] = get_object_or_404(self.model, pk=pk)
        return context


class UpdateView(View):
    template_name = None
    context_object_name = 'objects'
    pk_url_kwarg = 'pk'
    model = None
    class_form = None
    success_url = '/'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.class_form(instance=obj)
        return render(request, self.template_name, {'form': form, self.context_object_name: obj})

    def post(self, request, *args, **kwargs):
        data = request.POST
        self.obj = self.get_object()
        form = self.class_form(instance=self.obj, data=data)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(self.model, pk=pk)
        return obj

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, self.context_object_name: self.obj})


class DeleteView(View):
    model = None
    template_name = None
    confirm_template_name = None
    context_object_name = 'objects'
    success_url = '/'
    confirm_of_delete = None

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.confirm_template_name, {self.context_object_name: obj})

    def post(self, request, pk):
        if self.confirm_of_delete and 'confirm' not in request.POST:
            return self.get(request, pk)
        elif 'confirm' in request.POST:
            return self.delete_object(pk)
        else:
            return self.delete_object(pk)

    def delete_object(self, pk):
        obj = get_object_or_404(self.model, pk=pk)
        try:
            obj.delete()
            return redirect(self.success_url)
        except BaseException as error:
            return render(self.request, self.template_name, {'errors': error})

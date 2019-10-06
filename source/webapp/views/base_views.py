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
    context_key = 'objects'
    pk_url_kwarg = 'pk'
    model = None
    class_form = None
    success_url = '/'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(self.model, pk=pk)
        form = self.class_form(instance=obj)
        return render(request, self.template_name, {'form': form, self.context_key: obj})

    def post(self, request, *args, **kwargs):
        data = request.POST
        pk = kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(self.model, pk=pk)
        form = self.class_form(instance=obj, data=data)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form, self.context_key: obj})

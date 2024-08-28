from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render
from .models import AbonnementClient
from django.views.generic import (CreateView, DeleteView,DetailView,
                                 ListView, UpdateView)
from .forms import AbonnemetsClientModelForm
import json
from django.http import HttpResponse 
def abc_htmx_view(request):
    client_id = request.GET.get('client')
    template_name = "abc_hx.html"
    abcs=AbonnementClient.objects.filter(client__id=client_id)
    return render(request, template_name, {'abcs': abcs})


class CreateAbonnemtClient(CreateView):
    template_name = "_abonnements_client_form.html"
    form_class = AbonnemetsClientModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        client_pk = self.kwargs.get('pk')
        if client_pk:
            kwargs['initial'] = {'client_pk': client_pk}
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        posted_data = "\n.".join(f'{key}: {value}' for key, value in request.POST.items())
        print('POSTED DATA =========\n', posted_data, '\n==========')

        if form.is_valid():
            form.save()
            message = _("Abonnement Client crée avec succès")
            messages.success(request, str(message), extra_tags="toastr")
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    "closeModel": "kt_model",
                    "refresh_table": None
                })
            })
        else:
            print("Form is not valid", form.errors.as_data())
            context = {'form': form}
            return render(request, self.template_name, context)



from django.views.generic.base import TemplateView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView 
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Presence
from .tables import PresencesHTMxTable
from client.models import Client
from abonnement.models import AbonnementClient
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import PresenceManuelleModelForm
from django.views.generic import (CreateView, DeleteView,DetailView,
                                 ListView, UpdateView)
from django.shortcuts import render
from salle_activite.models import Salle,Activity,Door
import json
from .filters import PresenceFilter


class PresencesView(SingleTableMixin, FilterView):
    table_class = PresencesHTMxTable
    filterset_class=PresenceFilter
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["salles"]=Salle.objects.all()
        context["activites"]=Activity.objects.all()
        return context
    def get_template_names(self):
        
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "presences.html" 
        return template_name 

def presence_client(request):
    code_card=request.GET.get('search','')
    abc_list=AbonnementClient.objects.filter(client_id=code_card)
    for abc in abc_list:
        print('abc--------------------',abc)
        print("creneau------------",abc.creneaux)
    client_id=get_object_or_404(Client, id=code_card)
    if client_id :
        client_id.auto_presence()
    else :
        message = _("cilent a été créé avec succès.")
        messages.success(request, str(message),extra_tags="toastr")   
    return HttpResponse(status=204) 


class PresenceManuelleClient(CreateView):
    template_name = "snippets/_presence_Manuelle_form.html"
    form_class =PresenceManuelleModelForm

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
        posted_data = "\n.".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA =========\n', posted_data, '\n==========')
        
        if form.is_valid():
            print("is valide")
            paiement = form.save()
            message = _("Presence a été créé avec succès")
            messages.success(request, str(message), extra_tags="toastr")
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None
                })
            })
        else:
            print('is not valide', form.errors.as_data())
            client = request.POST.get('client')
            abcs= AbonnementClient.objects.filter(client=client)
            context = {'form': form}
            return render(request, self.template_name, context)




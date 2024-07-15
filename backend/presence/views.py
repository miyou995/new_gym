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



class PresencesView(SingleTableMixin, FilterView):
    table_class = PresencesHTMxTable
    model = Presence
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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




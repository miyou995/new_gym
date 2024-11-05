from django.views.generic.base import TemplateView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView 
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Presence
from .tables import PresencesHTMxTable
from django.db.models import Q
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
from django.urls import reverse_lazy
from .filters import PresenceFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import  permission_required


class PresencesView(PermissionRequiredMixin,SingleTableMixin, FilterView):
    permission_required = "presence.view_presence"
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
    
@permission_required("presence.add_presence" , raise_exception=True)
def presence_client(request):
    context= {}
    code=request.GET.get('search','')
    print("from client present//////////////////")
    client_id=Client.objects.filter(Q(id=code) | Q(carte=code))
    print("client_id---------------",client_id)
    # abc_list=AbonnementClient.objects.filter(client__carte=code)
    # for abc in abc_list:
    #     print('abc--------------------',abc)
    #     print("creneau------------",abc.creneaux)
    if client_id :
        print("client_id----------------")
        client_id=get_object_or_404(Client, Q(id=code) | Q(carte=code))
        auto_presence=client_id.auto_presence()
        context["client"]=client_id
        context["auto_presence"]=auto_presence
        if auto_presence == 'not_today':
            print("-------------------working from presence--------------------")
            return render(request,"snippets/presence_popup.html",context)
        elif auto_presence == 'entre':
            print("enter ------------------------------------")
            return render(request,"snippets/presence_popup.html",context)
        elif auto_presence == 'fin_abonnement':
            print("fin d'abonnemnt---------------------")
            return render(request,"snippets/presence_popup.html",context)
        elif auto_presence == 'sortie':
            print("la sortie---------------------")
            return render(request,"snippets/presence_popup.html",context)
    else :
        print(" else----------client_id----------------")
        message = _("client n'exist pas .")
        messages.warning(request, str(message),extra_tags="toastr")   
    return HttpResponse(status=204) 


class PresenceManuelleClient(PermissionRequiredMixin,CreateView):
    permission_required = "presence.add_presence"
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
            presence= form.save()
            ecart = presence.get_time_consumed(presence.hour_sortie)
            presence.abc.presence_quantity -= ecart
            presence.abc.save() 
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


class PresenceManuelleUpdateClient(PermissionRequiredMixin,UpdateView):
    permission_required = "presence.change_presence"
    model = Presence 
    template_name = "snippets/_presence_Manuelle_form.html"
    fields = [
                'abc',
                'creneau',
                'hour_entree',
                'hour_sortie',
                'date',
                'note',
    ]
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('yeah form instance', self.object)
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        presence =form.save()
        ecart = presence.get_time_consumed(presence.hour_sortie)
        presence.abc.presence_quantity -= ecart
        presence.abc.save() 
        print('IS FORM VALID', presence.id)
        messages.success(self.request, "Presence Mis a jour avec Succés",extra_tags="toastr")
        return HttpResponse(status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None,
                    "selected_client": f"{presence.id}",
                })
            }) 
    
    def form_invalid(self, form):
        messages.success(self.request, form.errors ,extra_tags="toastr")
        return self.render_to_response(self.get_context_data(form=form)) 


class PresenceManuelleDeleteClient(PermissionRequiredMixin,DeleteView):
    permission_required = "presence.delete_presence"
    model = Presence
    template_name = "snippets/delete_modal.html"
    def get_success_url(self):
        return reverse_lazy("client:client_detail", kwargs={'pk': str(self.object.abc.client.pk
                                                                      )})
    
    def form_valid(self, form):
        success_url=self.get_success_url()
        ecrat=self.object.get_time_consumed(self.object.hour_sortie)
        self.object.abc.presence_quantity += ecrat
        self.object.abc.save()
        self.object.delete()
        messages.success(self.request,"Presence Supprimier avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)


from django.db.models.query import QuerySet
from django.utils.translation import gettext as _
from django.shortcuts import redirect, render
from abonnement.mixins import CalendarAbonnementClientMixin
from abonnement.forms import AbonnementClientAddForm, AbonnementClientEditForm, AbonnementClientRestPaiementForm, AbonnementClientRestTempForm
from .models import Abonnement, AbonnementClient
import json
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_filters.views import FilterView
from .models import Creneau
from .filters import CalenderFilter
from django_filters.views import FilterView
from django.urls import reverse, reverse_lazy
from client.models import Client
from datetime import datetime, timedelta
from django_htmx.http import HttpResponseClientRedirect
from datetime import datetime,time,date
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.views.generic import  DeleteView
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib import messages
from transaction.models import Paiement
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required

def abc_htmx_view(request):
    client_id = request.GET.get('client')
    template_name = "abc_hx.html"
    abcs=AbonnementClient.objects.filter(client__id=client_id)
    response = render(request, template_name, {'abcs': abcs})
    response.headers={
                    'HX-Trigger': json.dumps({
                        "referesh_creneaux": None
                    })
                }
    return response


class CalendarAbonnementClient(PermissionRequiredMixin,CalendarAbonnementClientMixin):
    permission_required = 'abonnement.add_abonnementclient'
    
    def get_template_names(self):
        template_name = "abonnement_calendar.html"
        return template_name

    def get_queryset(self):
        return Creneau.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = get_object_or_404(Client, pk=self.kwargs['pk'])
        return context



class RetreiveAbonnementClient(PermissionRequiredMixin,CalendarAbonnementClientMixin):
    permission_required = 'abonnement.change_abonnementclient'
    filterset_class = CalenderFilter
    model = Creneau
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        abc = get_object_or_404(AbonnementClient, pk=self.kwargs['pk'])
        context["abc"]= abc
        context["seleced_events"] = abc.get_selected_events()
        context["form"] = AbonnementClientEditForm(instance=abc)
        return context
        
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['data'] = self.request.GET.copy()
        kwargs['data']['abc_id'] = self.kwargs['pk']  # Inject abc_id into filter data
        return kwargs
    
    def get_queryset(self) :
        abc = get_object_or_404(AbonnementClient, pk=self.kwargs['pk'])
        return Creneau.objects.filter(activity__salle__abonnements__id=abc.type_abonnement.id)
    
    def get_template_names(self):
        template_name = "snippets/update_calander.html"
        return template_name
    
    

@require_POST
def add_abonnement_client(request,client_pk,type_abonnement):
    form = AbonnementClientAddForm(request.POST, client_pk=client_pk)
    print('OUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
    if form.is_valid():
        
        print('Add abc Form is valid')
        form.save()
        message = _("Abonnement ajouter avec succès.")
        messages.success(request, str(message))
        return HttpResponse(status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": "kt_modal",
                        "refresh_abcs": None
                            
                    })
                }) 
    else :
        messages.error(request, form.errors)
        
        print("form.errores-------------->", form.errors)
    return redirect('abonnement:calendar_abonnement_client', kwargs={'pk': client_pk})

@require_POST
def update_abonnement_client(request,pk):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    form = AbonnementClientEditForm(request.POST, instance=abonnement_client)
    print('OUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
    if form.is_valid():
        print('Add abc Form is valid')
        form.save()
        message = _("Abonnement ajouter avec succès.")
        messages.success(request, str(message))
        return HttpResponse(status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": "kt_modal",
                        "refresh_abcs": None
                    })
                }) 
    else :
        messages.error(request, form.errors)
        
        print("form.errores-------------->", form.errors)
    return redirect('abonnement:calendar_abonnement_client', kwargs={'pk': pk})





class AbonnemtClientDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = 'abonnement.delete_abonnementclient'
    model = AbonnementClient
    template_name = "buttons/delete.html"
    def get_success_url(self):
        return reverse_lazy("client:client_detail", kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        success_url = self.get_success_url()
        paiment = Paiement.objects.filter(abonnement_client=self.object)
        if paiment :
            print("you can not delete this abc")
            messages.error(self.request, "Supprimer le paiement de cet abonnement pour avoir supprimer l'abonnement ")
            return HttpResponseRedirect(success_url)
        else :
            self.object.delete()
            print('GOOOOO')
            messages.success(self.request, "Abonnemet Client Supprimer avec Succés")
            return HttpResponseRedirect(success_url)



@require_POST
def update_temps_rest(request, pk):
    if request.method == "POST":
        print(list(request.POST.items()))
        product = get_object_or_404(AbonnementClient, pk=pk)
        form = AbonnementClientRestTempForm(request.POST, instance=product)
        if form.is_valid() :
            if form.is_valid():
                form.save()
            message = _("Reste temps updated successfully.")
            messages.success(request, str(message))
        else:
            message = _("Error occures when updating product.")
            messages.error(request, str(message))
        return JsonResponse({"success": True})



@require_POST
def update_paiement_rest(request, pk):
    if request.method == "POST":
        print(list(request.POST.items()))
        product = get_object_or_404(AbonnementClient, pk=pk)
        form = AbonnementClientRestPaiementForm(request.POST, instance=product)
        if form.is_valid() :
            if form.is_valid():
                form.save()
            message = _("Reste  updated successfully.")
            messages.success(request, str(message))
        else:
            message = _("Error occures when updating product.")
            messages.error(request, str(message))
        return JsonResponse({"success": True})


def renew_abonnement_client(request,pk):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    renouvle_date = request.POST.get('renouvle')
    if renouvle_date:
        print("get date-/-/-/-/-/-/-/-/-/-/-/-/-/-/",renouvle_date)
        abonnement_client.renew_abc(renouvle_date)
        print("renew is done ---------------------")
    return HttpResponse(status=204)


def block_deblock_abonnement_client(request,pk):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    block_date = request.POST.get('block_date')
    print("block_date------------->>>>>",block_date)
    if block_date :
        abonnement_client.lock(block_date)
        if not abonnement_client.blocking_date :
            print("-----------------------blocking date not correct")
            message = _("vous pouvez pas bloquer cette abonnement.")
            messages.warning(request, str(message))
            return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })
        message = _("l'abonnement est bloqué.")
        messages.success(request, str(message))    

    else :
        abonnement_client.unlock() 
        message = _("l'abonnement est débloqué.")
        messages.success(request, str(message))  
    return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })





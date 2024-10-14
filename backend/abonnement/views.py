from django.utils.translation import gettext as _
from django.shortcuts import redirect, render
from abonnement.mixins import CalendarAbonnementClientMixin
from abonnement.forms import AbonnementClientRestPaiementForm, AbonnementClientRestTempForm
from .models import Abonnement, AbonnementClient
import json
from django_filters.views import FilterView
from .models import Creneau
from .filters import CalenderFilter
from django_filters.views import FilterView
from django.urls import reverse, reverse_lazy
from client.models import Client
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django_htmx.http import HttpResponseClientRedirect
from datetime import datetime,time,date
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods
from django.views.generic import  DeleteView
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from transaction.models import Paiement
from django.http import JsonResponse




def abc_htmx_view(request):
    client_id = request.GET.get('client')
    template_name = "abc_hx.html"
    abcs=AbonnementClient.objects.filter(client__id=client_id)
    return render(request, template_name, {'abcs': abcs})


class CalendarAbonnementClient(CalendarAbonnementClientMixin):
    def get_template_names(self):
        template_name = "abonnement_calendar.html"
        return template_name

def add_abonnement_client(request,client_pk,type_abonnement):
    event_pk = request.POST.getlist('event_pk')
    event_pk = [int(pk) for pk in event_pk]  # Convert each item to an integer
    today_str = request.POST.get('today')
    if today_str:
            today = datetime.strptime(today_str, '%Y-%m-%d')  # Convert string to date object
    else:
            today = datetime.today()  # Use the current date if 'today' is not provided
    end_date = today + timedelta(days=30)
    # type_abonnement = request.POST.get('type_abonnement')
    client = get_object_or_404(Client, pk=client_pk)
    creneaux=Creneau.objects.filter(pk__in=event_pk)
    print("type_abonnement----------------", type_abonnement)
    if type_abonnement and type_abonnement != "None" and event_pk :
        print("form typeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        abonnement_Obj = get_object_or_404(Abonnement, pk=type_abonnement)
        print("client-----------------", client)
        print("type_abonnement----------------", type_abonnement)
        print("abonnement_Obj--------------", abonnement_Obj)
        print("event_pk----------------", event_pk)
        print("creneaux----------------", creneaux)
        print("today---------------",today)
        abonnement_client = AbonnementClient(
                start_date=today,
                end_date=end_date,
                client=client,
                type_abonnement=abonnement_Obj,
            )
        abonnement_client.save()
        abonnement_client.creneaux.set(creneaux)
        abonnement_client.save()
        redirect_url = reverse("client:client_detail", kwargs={'pk': client_pk})
        return HttpResponseClientRedirect(redirect_url)
    else :
         print("no type_abonnement or no selected event-------------->")
    return redirect('abonnement:calendar_abonnement_client', kwargs={'pk': client_pk})

class CalendarUpdateAbonnementClient(FilterView):
    filterset_class = CalenderFilter
    model = Creneau
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["events"] = json.dumps(self.get_events())
            abc = AbonnementClient.objects.filter(pk=self.kwargs['pk'])
            context["abc"]=get_object_or_404(AbonnementClient, pk=self.kwargs['pk'])
            print("abc*********************>>>>>>",context["abc"])
            # context["seleced_events"] = abc
            selected_events_data = list(abc.values('creneaux__pk', 'creneaux__name', 'creneaux__hour_start', 'creneaux__hour_finish','type_abonnement','start_date'))
            for event in selected_events_data:
                if isinstance(event.get('creneaux__hour_start'), datetime):
                    event['creneaux__hour_start'] = event['creneaux__hour_start'].isoformat()  # Convert datetime to ISO format
                if isinstance(event.get('creneaux__hour_finish'), datetime):
                    event['creneaux__hour_finish'] = event['creneaux__hour_finish'].isoformat()  # Convert datetime to ISO format
                if isinstance(event.get('creneaux__hour_start'), time):
                    event['creneaux__hour_start'] = event['creneaux__hour_start'].strftime('%H:%M:%S')  # Convert time to string
                if isinstance(event.get('creneaux__hour_finish'), time):
                    event['creneaux__hour_finish'] = event['creneaux__hour_finish'].strftime('%H:%M:%S')  # Convert time to string
                
                if isinstance(event.get('start_date'), datetime):
                    event['start_date'] = event['start_date'].date().isoformat()
                elif isinstance(event.get('start_date'), date):
                    event['start_date'] = event['start_date'].isoformat()

            print("selected_events_data--------------------",selected_events_data)
            context["seleced_events"] = json.dumps(selected_events_data)
            return context

    def get_events(self):
        abc = AbonnementClient.objects.filter(pk=self.kwargs['pk']).first()
        # events = self.filterset_class(self.request.GET, queryset=Creneau.objects.all()).qs
        events = self.filterset_class(self.request.GET, queryset=Creneau.objects.filter(activity__salle__abonnements__id=abc.type_abonnement.id)).qs
        day_name_to_weekday = {
            'LU': 1,  # Monday
            'MA': 2,  # Tuesday
            'ME': 3,  # Wednesday
            'JE': 4,  # Thursday
            'VE': 5,  # Friday
            'SA': 6,  # Saturday
            'DI': 0,  # Sunday
        }
        events_list = []
        for event in events:
            event_weekday = day_name_to_weekday.get(event.day.upper())
            if event_weekday is not None:
                events_list.append({
                    'pk_event':event.pk,
                    'title': event.name,
                    'color': event.color,
                    'startTime': event.hour_start.strftime('%H:%M:%S'),
                    'endTime': event.hour_finish.strftime('%H:%M:%S'),
                    'daysOfWeek': [event_weekday],  # Repeat weekly on this day
                     'url': reverse('creneau:update_creneau', kwargs={'pk': event.pk}),
                })
        return events_list
    def get_template_names(self):
        template_name = "snippets/update_calander.html"
        return template_name
    
@require_http_methods(["POST"])
def update_abonnement_client(request, pk, type_abonnement):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    print("presence_quantity-----------------------------------",abonnement_client.presence_quantity)
    event_pk = request.POST.getlist('event_pk')
    deselected_event_pk = request.POST.getlist('deselected_event_pk', [])  
    # Filter out any invalid or non-integer values
    event_pk = [int(pk) for pk in event_pk if pk.isdigit()]
    deselected_event_pk = [int(pk) for pk in deselected_event_pk if pk.isdigit()]
    print("Filtered event_pk-------------------->>", event_pk)
    print("Deselected event_pk-------------------->>", deselected_event_pk)
    today_str = request.POST.get('today')
    print("today_str-------------------->>", today_str)
    if today_str:
        today = datetime.strptime(today_str, '%Y-%m-%d')
    else:
        today = datetime.today()
    end_date = today + timedelta(days=30)

    existing_creneaux = abonnement_client.creneaux.all()
    new_creneaux = Creneau.objects.filter(pk__in=event_pk)
    combined_creneaux = set(existing_creneaux) | set(new_creneaux)  
    # Remove deselected events
    combined_creneaux = [creneau for creneau in combined_creneaux if creneau.pk not in deselected_event_pk]

    if type_abonnement and type_abonnement != "None" and combined_creneaux:
        abonnement_Obj = get_object_or_404(Abonnement, pk=type_abonnement)
        abonnement_client.start_date = today
        abonnement_client.end_date = end_date
        abonnement_client.type_abonnement = abonnement_Obj
        abonnement_client.creneaux.set(combined_creneaux)  
        abonnement_client.save()
        redirect_url = reverse("client:client_detail", kwargs={'pk': abonnement_client.client.pk})
        return HttpResponseClientRedirect(redirect_url)
    else:
        print("no updating -*********-*---******-")
    return redirect('abonnement:calendar_abonnement_client', kwargs={'pk': abonnement_client.client.pk})



class AbonnemtClientDeleteView(DeleteView):
    model = AbonnementClient
    template_name = "buttons/delete.html"
    def get_success_url(self):
        return reverse_lazy("client:client_detail", kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        success_url = self.get_success_url()
        paiment = Paiement.objects.filter(abonnement_client=self.object)
        if paiment :
            print("you can not delete this abc")
            messages.error(self.request, "Supprimer le paiement de cet abonnement pour avoir supprimer l'abonnement ",extra_tags="toastr")
            return HttpResponseRedirect(success_url)
        else :
            success_url = self.get_success_url()
            self.object.delete()
            print('GOOOOO')
            messages.success(self.request, "Abonnemet Client Supprimer avec Succés",extra_tags="toastr")
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
            messages.success(request, str(message), extra_tags="toastr")
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
            messages.success(request, str(message), extra_tags="toastr")
        else:
            message = _("Error occures when updating product.")
            messages.error(request, str(message))
        return JsonResponse({"success": True})


def renew_abonnemetn_client(request,pk):
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
            message = _("blocking date not correct")
            messages.error(request, str(message))

    else :
        abonnement_client.unlock()   
    return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })





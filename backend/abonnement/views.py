from django.utils.translation import gettext as _
from django.shortcuts import redirect, render
from abonnement.mixins import CalendarAbonnementClientMixin
from .models import Abonnement, AbonnementClient
from django.views.generic import (CreateView, DeleteView,DetailView,
                                 ListView, UpdateView)
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
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime,time,date

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
        events = self.filterset_class(self.request.GET, queryset=Creneau.objects.all()).qs
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
    

# class  UpdateAbonnementClient(UpdateView):
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

def update_abonnement_client(request, pk, type_abonnement):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    event_pk = request.POST.getlist('event_pk')
    event_pk = [int(pk) for pk in event_pk]

    today_str = request.POST.get('today')
    if today_str:
        today = datetime.strptime(today_str, '%Y-%m-%d')
    else:
        today = datetime.today()
    
    end_date = today + timedelta(days=30)
    creneaux = Creneau.objects.filter(pk__in=event_pk)
    if type_abonnement and type_abonnement != "None" and event_pk:
        abonnement_Obj = get_object_or_404(Abonnement, pk=type_abonnement)

        # Update fields
        abonnement_client.start_date = today
        abonnement_client.end_date = end_date
        abonnement_client.type_abonnement = abonnement_Obj
        abonnement_client.creneaux.set(creneaux)

        abonnement_client.save()
    
    return HttpResponse(status=204)





     


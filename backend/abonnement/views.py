from django.utils.translation import gettext as _
from django.shortcuts import redirect, render
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

def abc_htmx_view(request):
    client_id = request.GET.get('client')
    template_name = "abc_hx.html"
    abcs=AbonnementClient.objects.filter(client__id=client_id)
    return render(request, template_name, {'abcs': abcs})


class CalendarAbonnementClient(FilterView):
    filterset_class = CalenderFilter
    model = Creneau
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = json.dumps(self.get_events())
        context["client"] = get_object_or_404(Client, pk=self.kwargs['pk'])
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
        # if self.request.htmx:
        #     template_name = "snippets/calander_partial.html"
        # else:
        template_name = "abonnement_calendar.html"
        return template_name 
    
    
    def get(self, request, *args, **kwargs):
         return super().get(request, *args, **kwargs)
    


def add_abonnement_client(request,client_pk):
    event_pk = request.POST.getlist('event_pk')
    event_pk = [int(pk) for pk in event_pk]  # Convert each item to an integer
    today_str = request.POST.get('today')
    if today_str:
            today = datetime.strptime(today_str, '%Y-%m-%d')  # Convert string to date object
    else:
            today = datetime.today()  # Use the current date if 'today' is not provided
    end_date = today + timedelta(days=30)
    type_abonnement = request.POST.get('type_abonnement')
    client = get_object_or_404(Client, pk=client_pk)
    creneaux=Creneau.objects.filter(pk__in=event_pk)
    if type_abonnement :
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
    return redirect('calander_partial.html')  






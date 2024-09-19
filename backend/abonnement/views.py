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
            abc = AbonnementClient.objects.filter(client=self.kwargs['pk'])
            print("client*********************>>>>>>",abc)
            context["client"] = abc 
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
    

class  UpdateAbonnementClient(UpdateView):
    model = AbonnementClient
    fields = ['type_abonnement']
    # template_name = "snippets/update_calander.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get selected events for this client
        selected_events = list(self.object.creneaux.values_list('pk', flat=True))  # Assuming Creneaux is ManyToMany
        # Fetch all events for the calendar
        all_events = Creneau.objects.all().values('pk', 'name', 'hour_start', 'hour_finish')

        # Add both the selected events and all events to the context
        context['events'] = json.dumps(list(all_events), cls=DjangoJSONEncoder)  # Send events as JSON
        context['selected_events'] = selected_events  # Send selected event PKs
        print("events---------------",context)

        return context

    def post(self, request, *args, **kwargs):
        # Fetch the existing AbonnementClient object to update
        self.object = self.get_object()
        type_abonnement = request.POST.get('type_abonnement')
        selected_events = request.POST.getlist('event_pk[]')  # Get the selected events (Creneaux)
        today = request.POST.get('today')

        # Update the abonnement field
        self.object.abonnement = type_abonnement

        # Update selected Creneaux (events)
        if selected_events:
            creneaux = Creneau.objects.filter(pk__in=selected_events)
            self.object.creneaux.set(creneaux)  # Assuming ManyToMany relationship
            self.object.save()

        # Return a JSON response
        return JsonResponse({
            'status': 'success',
            'message': 'AbonnementClient updated successfully!',
        })





     


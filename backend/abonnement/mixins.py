from django_filters.views import FilterView
from .filters import CalenderFilter
from .models import AbonnementClient, Creneau
from django.shortcuts import get_object_or_404
from client.models import Client
import json
from django.urls import reverse

class CalendarAbonnementClientMixin(FilterView):
    filterset_class = CalenderFilter
    model = Creneau
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = json.dumps(self.get_events())
        # abc = AbonnementClient.objects.filter(client=self.kwargs['pk'])
        # print("client*********************>>>>>>",abc)
        # context["client"] = abc 
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
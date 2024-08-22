from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse

from planning.models import Planning
from .models import Creneau
from datetime import datetime, timedelta
from salle_activite.models import Salle




def calendar_view(request):
    context={}
    context["Plannings"]=Planning.objects.all()
    context["salles"]=Salle.objects.all()
    return render(request, 'creneaux.html',context)



def event_data(request):
    # Get the selected planning and salle from the query parameters
    planning_id = request.GET.get('planning')
    salle_id = request.GET.get('salle')

    # Filter the events based on the selected planning and salle
    events = Creneau.objects.all()
    if planning_id:
        events = events.filter(planning_id=planning_id)
    if salle_id:
        events = events.filter(salle_id=salle_id)

    # Mapping day names to weekday numbers for FullCalendar (Sunday is 0, Monday is 1)
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
                'title': event.name,
                'startTime': event.hour_start.strftime('%H:%M:%S'),
                'endTime': event.hour_finish.strftime('%H:%M:%S'),
                'daysOfWeek': [event_weekday],  # Repeat weekly on this day
            })

    return JsonResponse(events_list, safe=False)

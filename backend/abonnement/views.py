from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Abonnement, AbonnementClient
from django.views.generic import (CreateView, DeleteView,DetailView,
                                 ListView, UpdateView)
import json
from django.http import HttpResponse 
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
        # print("events_list------------------------------",events_list)
        return events_list
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "calander_partial.html"
        else:
            template_name = "snippets/abonnement_calendar.html"
        return template_name 





def add_abonnement_client(request,client_pk):
    
    # abonnement_id = self.request.GET.get('abonnement')
    print("add_abonnement_client-----------------------------------------------")
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
    abonnement_Obj = get_object_or_404(Abonnement, pk=type_abonnement)
    

    print("client-----------------", client)
    print("type_abonnement----------------", type_abonnement)
    print("abonnement_Obj--------------", abonnement_Obj)
    print("event_pk----------------", event_pk)
    print("creneaux----------------", creneaux)
    print("today---------------",today)

      # Create the AbonnementClient instance
    abonnement_client = AbonnementClient(
            start_date=today,
            end_date=end_date,  # Assuming end_date is optional and might be set later
            client=client,
            type_abonnement=abonnement_Obj,
        )
    abonnement_client.save()
        
        # Set the many-to-many relationship for creneaux
    abonnement_client.creneaux.set(creneaux)
        
        # Optionally, save again if needed
    abonnement_client.save()

        # Redirect or return a response after saving
    return redirect('calander_partial.html')  # Change 'some_view_name' to your actual view







    # filterset_class = CalenderFilter
    # # template_name = "_abonnements_client_form.html"
    # form_class = AbonnemetsClientModelForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     client_pk = self.kwargs.get('pk')
    #     print(f"Client PK------------------------------------: {client_pk}")  
    #     if client_pk:
    #         kwargs['initial'] = {'client_pk': client_pk}
    #     return kwargs

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(**self.get_form_kwargs())
    #     context = {
    #         "form": form,
    #     }
    #     print("work from gettttttttttttttttttttttttttttttttttt")
    #     return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(data=request.POST)
    #     posted_data = "\n.".join(f'{key}: {value}' for key, value in request.POST.items())
    #     print('POSTED DATA ===============================\n', posted_data, '\n==========')

    #     if form.is_valid():
    #         form.save()
    #         print("form is saveddddddddddddddddddddddddddd")
    #         message = _("Abonnement Client crée avec succès")
    #         messages.success(request, str(message), extra_tags="toastr")
    #         return HttpResponse(status=204, headers={
    #             'HX-Trigger': json.dumps({
    #                 "closeModel": "kt_model",
    #                 "refresh_table": None
    #             })
    #         })
    #     else:
    #         print("Form is not valid", form.errors.as_data())
    #         print("form not validdddddddddddddddddddddddddd")
    #         context = {'form': form}
    #         return render(request, self.template_name, context)






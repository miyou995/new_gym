import json
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (CreateView, DeleteView,UpdateView)
from .models import Creneau
from .forms import CreneauModelForm 
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from .filters import CalenderFilterCreneau
from django_filters.views import FilterView
from abonnement.models import AbonnementClient
from django_tables2 import SingleTableMixin
from .tables import AbonnementClientHTMxTable
from django.db.models import Max



class CreateCreneau(CreateView):
    template_name ="snippets/_creneau_form.html"
    form_class=CreneauModelForm 

    def get(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        posted_data = "\n.".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA =========\n', posted_data, '\n==========')
        if form.is_valid():
            form.save()
            message = _("Creneau a été créé avec succès")
            messages.success(request, str(message), extra_tags="toastr")
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None
                })
            })
        else :
            print('is not valide', form.errors.as_data())
            context = {'form': form}
            return render(request, self.template_name, context)

class UpdateCreneau(UpdateView):
        model=Creneau
        template_name ="snippets/_creneau_form.html"
        form_class =CreneauModelForm
    
        def get(self, request, *args, **kwargs):
            self.object = self.get_object()
            print('yeah form instance', self.object)
            return super().get(request, *args, **kwargs)
        def form_valid(self, form):
            paiement =form.save()
            print('IS FORM VALID', paiement.id)
            messages.success(self.request, "Creneau Mis a jour avec Succés",extra_tags="toastr")
            return HttpResponse(status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": "kt_modal",
                        "refresh_table": None,
                        
                    })
                }) 
    
        def form_invalid(self, form):
            messages.success(self.request, form.errors)
            return self.render_to_response(self.get_context_data(form=form))   

class CreneauDeleteView(DeleteView):
    model = Creneau
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("creneau:creneaux_name")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        print('GOOOOO')
        messages.success(self.request, "Creneau Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    

class CalenderView(FilterView):
    filterset_class = CalenderFilterCreneau
    model = Creneau

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter'] = self.filterset
        context["events"] = json.dumps(self.get_events())
        # print('Called vevnets', context["events"])
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
                    'title': event.name,
                    'color': event.color,
                    'startTime': event.hour_start.strftime('%H:%M:%S'),
                    'endTime': event.hour_finish.strftime('%H:%M:%S'),
                    'daysOfWeek': [event_weekday],  # Repeat weekly on this day
                    'url': reverse('creneau:update_creneau', kwargs={'pk': event.pk}),
                   
                })
        return events_list
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "snippets/calender_partial.html"
        else:
            template_name = "snippets/calendar.html"
        return template_name 


class AbonnementsParCreneau(SingleTableMixin,FilterView):
    table_class = AbonnementClientHTMxTable
    model = AbonnementClient

    def get_queryset(self):
        creneau_pk = self.kwargs.get('pk')
        print("creneau_pk-------------", creneau_pk)
        # Annotate with the max created_date_time for each client
        latest_abonnements = AbonnementClient.objects.filter(creneaux__pk=creneau_pk).values('client') \
            .annotate(latest_created_date_time=Max('created_date_time'))
        # Filter original queryset with the annotated max created_date_time
        queryset = AbonnementClient.objects.select_related('client', 'type_abonnement') \
            .filter(creneaux__pk=creneau_pk, created_date_time__in=[item['latest_created_date_time'] for item in latest_abonnements]) \
            .order_by('-created_date_time')
        print("queryset....................>>", queryset)
        return queryset
   
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "snippets/_creneau_form.html" 
        return template_name
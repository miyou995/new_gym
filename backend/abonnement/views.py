from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render
from .models import AbonnementClient
from django.views.generic import (CreateView, DeleteView,DetailView,
                                 ListView, UpdateView)
from .forms import AbonnemetsClientModelForm
import json
from django.http import HttpResponse 
from planning.models import Planning
from salle_activite.models import Salle
from creneau.filters import CalenderFilter
from django_filters.views import FilterView
from .models import Creneau
from creneau.filters import CalenderFilter
from django_filters.views import FilterView
from django.urls import reverse, reverse_lazy


def abc_htmx_view(request):
    client_id = request.GET.get('client')
    template_name = "abc_hx.html"
    abcs=AbonnementClient.objects.filter(client__id=client_id)
    return render(request, template_name, {'abcs': abcs})


class CreateAbonnemtClient(FilterView):
    template_name="_abonnements_client_form.html"
    filterset_class = CalenderFilter
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
            template_name = "_abonnements_client_form.html"
        return template_name 

    # filterset_class = CalenderFilter
    # template_name = "_abonnements_client_form.html"
    # form_class = AbonnemetsClientModelForm


    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     client_pk = self.kwargs.get('pk')
    #     print(f"Client PK------------------------------------: {client_pk}")  #
    #     if client_pk:
    #         kwargs['initial'] = {'client_pk': client_pk}
    #     return kwargs

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(**self.get_form_kwargs())
    #     context = {
    #         "form": form,
    #         "Plannings": Planning.objects.all(),
    #         "salles": Salle.objects.all()
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






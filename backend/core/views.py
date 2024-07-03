from django.shortcuts import render
from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django.views.generic import (TemplateView,UpdateView,DeleteView)
from .tables import PlannigHTMxTable,SalleHTMxTable,ActivityHTMxTable,MaladieHTMxTable,PortesHTMxTable,AbonnementHTMxTable
from planning.models import Planning
from salle_activite.models import Salle,Activity,Door
from client.models import Maladie
from abonnement.models import Abonnement
from .forms import PlanningModelForm
from django.contrib import messages
from django.http import HttpResponse
import json
from django.utils.translation import gettext_lazy as _



class IndexView(TemplateView):
    print('=========== we are here')
    template_name = "index.html"



class GenericTableView(SingleTableMixin, FilterView):
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context if needed
        return context
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "configuration/configuration.html"
        return template_name 
    
class PlanningTable(GenericTableView):
    model = Planning
    table_class = PlannigHTMxTable

class SalleTable(GenericTableView):
    model = Salle
    table_class = SalleHTMxTable

class ActivityTable(GenericTableView):
    model = Activity
    table_class = ActivityHTMxTable

class MaladieTable(GenericTableView):
    model = Maladie
    table_class =MaladieHTMxTable

class PortesTable(GenericTableView):
    model = Door
    table_class =PortesHTMxTable

class MaladieTalble(GenericTableView):
    model = Maladie
    table_class =MaladieHTMxTable


class AbonnementTable(GenericTableView):
    model = Abonnement
    table_class =AbonnementHTMxTable


def PlanningCreateView(request):
    context = {}
    template_name = "configuration\snippets\_ajout_planning_form.html"
    form = PlanningModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = PlanningModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            client = form.save()
            message = _("Planning a été créé avec succès.")
            messages.success(request, str(message),extra_tags="toastr")
            return HttpResponse(status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": "kt_modal",
                        "refresh_table": None
                         
                    })
                }) 
        else:
            print("is not valide", form.errors.as_data())
            context["form"]=PlanningModelForm(data=request.POST or None )
            return render(request, template_name="configuration\snippets\_ajout_planning_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)

class PlanningUpdateView(UpdateView):
    model = Planning
    template_name="configuration\snippets\_ajout_planning_form.html"
    fields=[
        "name",
        "is_default"
   
    ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        client=form.save()
        print("is from valid",client.id)
        messages.success(self.request,"Planning Mis a jour avec Succés",extra_tags="toastr")
        return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })
    def form_invalid(self, form):
        messages.success(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))   
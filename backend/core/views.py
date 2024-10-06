from django.shortcuts import render
from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from transaction.models import Paiement
from django_tables2 import SingleTableMixin
from django.views.generic import (TemplateView,UpdateView,DeleteView)
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .tables import PlannigHTMxTable,SalleHTMxTable,ActivityHTMxTable,MaladieHTMxTable,PortesHTMxTable,AbonnementHTMxTable
from planning.models import Planning
from salle_activite.models import Salle,Activity,Door
from client.models import Client, Maladie
from abonnement.models import Abonnement, AbonnementClient
from .forms import PlanningModelForm,SalleModelForm,MaladieModelForm,ActiviteModelForm,DoorModelForm,AbonnementModelForm
from django.contrib import messages
from django.http import HttpResponse
import json
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum



class IndexView(TemplateView):
    print('=========== we are here')
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_dettes = AbonnementClient.objects.aggregate(total_reste=Sum('reste'))['total_reste'] or 0
        context['total_dettes'] = total_dettes

        chiffre_affaire = Paiement.objects.aggregate(total_chiffre=Sum('amount'))['total_chiffre'] or 0
        context["chiffre_affaire"] = chiffre_affaire

        total_clients = Client.objects.count()
        context["total_clients"] = total_clients 
        return context
    





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


# planning--------------------------------------------------------------------------------------
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
    
class PlanningDeleteView(DeleteView):
    model = Planning
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("core:PlanningTable")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        print('GOOOOO')
        messages.success(self.request, "Planning Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    
# salle----------------------------------------------------------------------------------------------
def SalleCreateView(request):
    context = {}
    template_name = "configuration\snippets\_ajout_Salle_form.html"
    form = SalleModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = SalleModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            client = form.save()
            message = _("Salle a été créé avec succès.")
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
            context["form"]=SalleModelForm(data=request.POST or None )
            return render(request, template_name="configuration\snippets\_ajout_Salle_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)

class SalleUpdateView(UpdateView):
    model = Salle
    template_name="configuration\snippets\_ajout_Salle_form.html"
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
        messages.success(self.request,"Salle Mis a jour avec Succés",extra_tags="toastr")
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
    

class SalleDeleteView(DeleteView):
    model = Salle
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("core:PlanningTable")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        print('GOOOOO')
        messages.success(self.request, "Salle Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    
# Activites------------------------------------------------------------------------------------------
def ActiviteCreateView(request):
    context = {}
    template_name = "configuration\snippets\_ajout_activites_form.html"
    form = ActiviteModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = ActiviteModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            client = form.save()
            message = _("Activite a été créé avec succès.")
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
            context["form"]=ActiviteModelForm(data=request.POST or None )
            return render(request, template_name="configuration\snippets\_ajout_activites_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)

class ActiviteUpdateView(UpdateView):
    model = Activity
    template_name="configuration\snippets\_ajout_activites_form.html"
    form_class= ActiviteModelForm
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        client=form.save()
        print("is from valid",client.id)
        messages.success(self.request,"Activite Mis a jour avec Succés",extra_tags="toastr")
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
    

class ActiviteDeleteView(DeleteView):
    model = Activity
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("core:PlanningTable")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        print('GOOOOO')
        messages.success(self.request, "Activite Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    
# Maladie--------------------------------------------------------------------------------------------

def MaladieCreateView(request):
    context = {}
    template_name = "configuration\snippets\_ajout_Maladies_form.html"
    form = MaladieModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = MaladieModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            client = form.save()
            message = _("Maladie a été créé avec succès.")
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
            context["form"]=MaladieModelForm(data=request.POST or None )
            return render(request, template_name="configuration\snippets\_ajout_maladies_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)

class MaladieUpdateView(UpdateView):
    model = Maladie
    template_name="configuration\snippets\_ajout_maladies_form.html"
    fields=[
        "name",
    ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        client=form.save()
        print("is from valid",client.id)
        messages.success(self.request,"Maladie Mis a jour avec Succés",extra_tags="toastr")
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
    

class MaladieDeleteView(DeleteView):
    model = Maladie
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("core:PlanningTable")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        print('GOOOOO')
        messages.success(self.request, "Maladie Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    
#Portes--------------------------------------------------------------------------------------------------
def PorteCreateView(request):
    context = {}
    template_name = "configuration\snippets\_ajout_ ports_form.html"
    form = DoorModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = DoorModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            client = form.save()
            message = _("Porte a été créé avec succès.")
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
            context["form"]=DoorModelForm(data=request.POST or None )
            return render(request, template_name="configuration\snippets\_ajout_ ports_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)

class PorteUpdateView(UpdateView):
    model = Door
    template_name="configuration\snippets\_ajout_ ports_form.html"
    fields=[
           'ip_adress',
            'salle',
            'username',
            'password'
    ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        client=form.save()
        print("is from valid",client.id)
        messages.success(self.request,"Porte Mis a jour avec Succés",extra_tags="toastr")
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
    

class PorteDeleteView(DeleteView):
    model = Door
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("core:PlanningTable")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        print('GOOOOO')
        messages.success(self.request, "Porte Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    
# Abonnement-------------------------------------------------------------------------------------------------
def TypeAbonnementCreateView(request):
    context = {}
    template_name = "configuration\snippets\_type_abonne_form.html"
    form = AbonnementModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = AbonnementModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            client = form.save()
            message = _("abonnement a été créé avec succès.")
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
            context["form"]=AbonnementModelForm(data=request.POST or None )
            return render(request, template_name="configuration\snippets\_type_abonne_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)

class TypeAbonnementUpdateView(UpdateView):
    model = Abonnement
    template_name="configuration\snippets\_type_abonne_form.html"
    form_class=AbonnementModelForm
    # fields=[
          
    #         'name',
    #         'price',
    #         'length',
    #         'seances_quantity',
    #         'salles',
    # ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        client=form.save()
        print("is from valid",client.id)
        messages.success(self.request,"Abonnement Mis a jour avec Succés",extra_tags="toastr")
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
    

class TypeAbonnementDeleteView(DeleteView):
    model = Abonnement
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("core:PlanningTable")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        print('GOOOOO')
        messages.success(self.request, "Abonnement Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)



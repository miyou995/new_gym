from typing import Dict
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import (CreateView, DeleteView,DetailView,
                                 ListView, UpdateView)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from abonnement.models import AbonnementClient
from .forms import PaiementModelForm,Remuneration_PersonnelModelForm,Remunération_CoachModelForm,Autre_TransactionForm
import json
from  django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .models import Paiement,RemunerationProf,Remuneration,Autre
from .tables import PiaementHTMxTable,RemunerationProfHTMxTable,RemunerationPersonnelHTMxTable
from .filters import ProductFilter,PersonnelFilter,CoachFilter


# tables views
class TransactionView(SingleTableMixin, FilterView):
    table_class = PiaementHTMxTable
    filterset_class = ProductFilter
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_url"]   = reverse('transactions:transaction_name')
        context["target"]       = "#table1"
        context["render_filter"]=ProductFilter(self.request.GET)
        return context

    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/transactions_table_partial.html"
        else:
            template_name = "transaction.html" 
        return template_name 


class RemunerationProfTable(SingleTableMixin, FilterView):
    table_class = RemunerationProfHTMxTable
    filterset_class = CoachFilter
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_url"]   = reverse('transactions:RemunerationProfTable_name')
        context["target"]       = "#table3"
        context["render_filter"]=CoachFilter(self.request.GET)
        return context
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/transactions_table_partial.html"
        else:
            template_name = "transaction.html"
        return template_name 


class RemunerationPersonnelTable(SingleTableMixin, FilterView):
    table_class = RemunerationPersonnelHTMxTable
    filterset_class = PersonnelFilter
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_url"]   = reverse('transactions:RemunerationPersonnelTable_name')
        context["target"]       = "#table2"
        context["render_filter"]=PersonnelFilter(self.request.GET)
        return context
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/transactions_table_partial.html"
        else:
            template_name = "transaction.html"
        return template_name 


class Chiffre_affaireView(TemplateView):
    template_name = "chiffre_affaire.html"

# paiement transactions------------------------------------------------------------------------------------------
def paiement(request):
    context = {}
    template_name = "snippets/_transaction_paiement_form.html"
    form = PaiementModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = PaiementModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            product = form.save()
            message = _("un paiement a été créé avec succès.")
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
            client = request.POST.get('client')
            abcs= AbonnementClient.objects.filter(client=client)
            context["form"] = PaiementModelForm(data=request.POST or None) 
            return render(request, template_name="snippets/_transaction_paiement_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)
  
class PaiementUpdateView(UpdateView):
    model = Paiement 
    template_name = "snippets/_transaction_paiement_form.html"
    fields = [
      
        'abonnement_client',
        'amount', 
        'notes',
    ]
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('yeah form instance', self.object)
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        paiement =form.save()
        print('IS FORM VALID', paiement.id)
        messages.success(self.request, "paiement Mis a jour avec Succés",extra_tags="toastr")
        return HttpResponse(status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None,
                    "selected_client": f"{paiement.id}",
                })
            }) 
    
    def form_invalid(self, form):
        messages.success(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))   

class PaiementDeleteView(DeleteView):
    model = Paiement
    template_name = "snippets/delete_modal.html"
    success_url = reverse_lazy("transactions:transaction_name")
    

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]= f"Paiement"
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Paiement Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
 

#remuneration personnel ------------------------------------------------------------------------------------------
def Remuneration_Personnel(request):
    context={} 
    template_name="snippets/_remu_personnel_form.html"
    form=Remuneration_PersonnelModelForm(data=request.POST or None)
    if request.method =="POST" :
        form= Remuneration_PersonnelModelForm(data=request.POST)
        posted_data="\n".join(f'{key} {value}' for key,value in request.POST.items())
        print('POSTED DATA =====\n',posted_data,'\n=====')
        if form.is_valid():
            print('is valide')
            product=form.save()
            message=_("une Remuneration Personnel a été créé avec succès")
            messages.success(request,str(message),extra_tags="toastr")
            return HttpResponse(status=204,
                                headers={
                                    'HX-Trigger':json.dumps({
                                        "closeModal":"kt_modal",
                                        "refresh_table":None
                                    })
                                })

        else:
            print("is not valide",form.errors.as_data())
            personnel=request.POST.get('nom')
            context["form"]=Remuneration_PersonnelModelForm(data=request.POST or None )
            return render(request,template_name="snippets/_remu_personnel_form.html", context=context)
    context["form"]=form
    return render(request,template_name=template_name,context=context)

class RemuPersonnelUpdateView(UpdateView):
    model=Remuneration
    template_name="snippets/_remu_personnel_form.html"
    fields=[
        'amount', 
        'notes',
    ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        remuneration=form.save()
        print("is from valid",remuneration.id)
        messages.success(self.request,"remuniration Personnel Mis a jour avec Succés",extra_tags="toastr")
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

class RemuPersonnelDeleteView(DeleteView):
    model =Remuneration
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy("transactions:RemunerationPersonnelTable_name")
 
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]= f"Personnel"
        return context

    def form_valid(self,form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Remuniration Personnel Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)

#remuneration Coach ------------------------------------------------------------------------------------------
def Remuneration_Coach(request):
    context={}
    template_name="snippets/_remu_Coach_form.html"
    form=Remunération_CoachModelForm(data=request.POST or None)
    if request.method=="POST":
        form=Remunération_CoachModelForm(data=request.POST)
        posted_data="\n.".join(f'{key} {value}' for key,value in request.POST.items())
        print('POSTED DATA =========\n',posted_data, '\n==========')
        if form.is_valid():
            print("is valide")
            remuniration=form.save()
            message=_("Remuniration Coach a été créé avec succès")
            messages.success(request,str(message),extra_tags="toastr")
            return HttpResponse(status=204,
                headers={
                    'HX-Trigger' :json.dumps({
                        "closeModal":"kt_modal",
                        "refresh_table":None

                    })
                })
        else:
            print('is not valide',form.errors.as_data())
            coach=request.POST.get("coach")
            context['form']=Remunération_CoachModelForm(data=request.POST or None)
            return render(request,template_name="snippets/_remu_Coach_form.html",context=context)
    context["form"]=form
    return render(request,template_name=template_name,context=context)

    
class Remuneration_CoachUpdateView(UpdateView):
    model=RemunerationProf
    template_name="snippets/_remu_Coach_form.html"
    fields=[
        'amount',
        'notes',
    ]
    def get(self,request,*args, **kwargs):
        self.object=self.get_object()
        print('from instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self, form):
        remuCoach=form.save()
        print('is from valid',remuCoach.id)
        messages.success(self.request,"Remuneration Coach Mis a jour avec Succés ",extra_tags="toastr")
        return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None,

                })
            })
    def form_invalid(self, form):
        messages.success(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))   
    

class RemCoachDeleteView(DeleteView):
    model =RemunerationProf
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy("transactions:RemunerationProfTable_name")

    def get_context_data(self,**kwargs):
    
        context=super().get_context_data(**kwargs)
        context["title"]= f"Coach"
        return context

    def form_valid(self,form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Remuniration Coach Supprimer avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)

# Auter Transaction------------------------------------------------------------------------------------------
def Autre_Transaction(request):
    context={}
    template_name="snippets/_autre_Transaction_form.html"
    
    form=Autre_TransactionForm(data=request.POST or None)
    if request.method=="POST":
        form=Autre_TransactionForm(data=request.POST)
        posted_data="\n.".join(f'{key} {value}' for key,value in request.POST.items())
        print('POSTED DATA =========\n',posted_data, '\n==========')
        if form.is_valid():
            print("is valide")
            remuniration=form.save()
            message=_("Autre transaction created successfully")
            messages.success(request,str(message),extra_tags="toastr")
            return HttpResponse(status=204,
                headers={
                    'HX-Trigger' :json.dumps({
                        "closeModal":"kt_modal",
                        "refresh_table":None

                    })
                })
        else:
            print('is not valide',form.errors.as_data())
            coach=request.POST.get("name")
            context['form']=Autre_TransactionForm(data=request.POST or None)
            return render(request,template_name="snippets/_autre_Transaction_form.html",context=context)
    context["form"]=form
    return render(request,template_name=template_name,context=context)

class Autre_TransactionUpdateView(UpdateView):
    model=Autre
    template_name="snippets/_autre_Transaction_form.html"
    fields=[
        'amount', 
        'name',
        'notes',
    ]
    def get(self,request,*args, **kwargs):
        self.object=self.get_object()
        print("from instance",self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        autre=form.save()
        print('is form valide',Autre.id)
        messages.success(self.request,"Autre transactions Mis A Jour avec Succés",extra_tags="toastr")
        return HttpResponse(statu=204,
                headers={
                    'HX-Trigger':json.dumps({
                        "closeModal":"kt_modal",
                        "refresh_table":None,

                    })
                })
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return self.render_to_response(self.get_context_data(form=form))



    


    
















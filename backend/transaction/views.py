from typing import Dict
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import (CreateView, DeleteView,DetailView,
                                 ListView, UpdateView)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from abonnement.models import AbonnementClient
from .forms import PaiementModelForm,Remuneration_PersonnelModelForm,Remunération_CoachModelForm,Autre_TransactionForm
import json
from  django_tables2 import SingleTableMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django_filters.views import FilterView
from .models import Paiement,RemunerationProf,Remuneration,Autre
from .tables import PiaementHTMxTable,RemunerationProfHTMxTable,RemunerationPersonnelHTMxTable,AutreTransactionTableHTMxTable
from .filters import ProductFilter,PersonnelFilter,CoachFilter,AutreTransactionFilter
from django.contrib.auth.decorators import  permission_required
from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render



# tables views
class TransactionView(PermissionRequiredMixin,SingleTableMixin, FilterView):
    permission_required ="transaction.view_transaction"
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


class RemunerationProfTable(PermissionRequiredMixin,SingleTableMixin, FilterView):
    permission_required ="transaction.view_remunerationprof"
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


class RemunerationPersonnelTable(PermissionRequiredMixin,SingleTableMixin, FilterView):
    permission_required ="transaction.view_remuneration"
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

class AutreTransactionTable(PermissionRequiredMixin,SingleTableMixin,FilterView):
    permission_required = "transaction.view_autre"
    table_class=AutreTransactionTableHTMxTable
    filterset_class=AutreTransactionFilter
    paginate_by=15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_url"]   = reverse('transactions:autre_transaction_table')
        context["target"]       = "#table4"
        context["render_filter"]=AutreTransactionFilter(self.request.GET)
        return context
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/transactions_table_partial.html"
        else:
            template_name = "transaction.html"
        return template_name 



class chiffre_affaire(PermissionRequiredMixin,TemplateView):
    permission_required = "transaction.can_view_statistique"
    template_name = "chiffre_affaire.html"


def chiffre_par_abonnement(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    paiement_queryset = Paiement.objects.all()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        paiement_queryset = paiement_queryset.filter(date_creation__range=[start_date, end_date])

    # Aggregate after applying date filter
    subscription_totals = (paiement_queryset
        .values('abonnement_client__type_abonnement__name')
        .annotate(total=Sum('amount'))
        .order_by('abonnement_client__type_abonnement__name'))
    # Prepare data for JSON response
    labels = [item['abonnement_client__type_abonnement__name'] for item in subscription_totals]
    amounts = [float(item['total']) for item in subscription_totals]
    total = sum(amounts)
    # print('subscription_totals-------------', subscription_totals)
    return render(request, 'snippets/chart_graph.html', {
        'subscription_totals': subscription_totals,
        'chart_labels': labels,
        'chart_data': amounts,
        "id": "subscriptionChart",
        "title": "Chiffre d'affaire par Abonnement",
        "total": total,
        
    })

def chifre_dattes_abonnement(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    paiement_queryset = AbonnementClient.objects.all()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
        paiement_queryset = paiement_queryset.filter(created_date_time__range=[start_date, end_date])


    reste_abn_totals = (paiement_queryset
        .values('type_abonnement__name')
        .annotate(total=Sum('reste'))
        .order_by('type_abonnement__name'))

    abbonnement_labels = [str(item['type_abonnement__name']) for item in reste_abn_totals]
    abonnement_reste = [float(item['total']) for item in reste_abn_totals]
    # print('reste_abn_totals---------------', reste_abn_totals)
    total = sum(abonnement_reste)
    return render(request, 'snippets/chart_graph.html', {
        'room_totals': reste_abn_totals,
        'chart_labels': abbonnement_labels,
        'chart_data': abonnement_reste,
        "id" : "resteChart",
        "title" : "Dettes par  abonnement",
        "total": total,
    })

def chiffre_par_Activity(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    paiement_queryset = Paiement.objects.all()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        paiement_queryset = paiement_queryset.filter(date_creation__range=[start_date, end_date])

    room_totals = (paiement_queryset
        .values('abonnement_client__creneaux__activity__name')
        .annotate(total=Sum('amount'))
        .order_by('abonnement_client__creneaux__activity__name'))

    room_labels = [str(item['abonnement_client__creneaux__activity__name']) for item in room_totals]
    room_amounts = [float(item['total']) for item in room_totals]
    # print('room_totals', room_totals) 
    total = sum(room_amounts)
    return render(request, 'snippets/chart_graph.html', {
        'room_totals': room_totals,
        'chart_labels': room_labels,
        'chart_data': room_amounts,
        "id" : "roomChart",
        "title" : "Chiffre d'affaire par Activité",
        "total": total,
    })



# paiement transactions------------------------------------------------------------------------------------------
class paiement(PermissionRequiredMixin,CreateView):
    permission_required = "transaction.add_paiement"
    template_name = "snippets/_transaction_paiement_form.html"
    form_class =PaiementModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        client_pk = self.kwargs.get('pk')
        if client_pk:
            kwargs['initial'] = {'client_pk': client_pk}
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        posted_data = "\n.".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA =========\n', posted_data, '\n==========')
        
        if form.is_valid():
            print("is valide")
            paiement = form.save()
            message = _("un paiement a été créé avec succès")
            messages.success(request, str(message))
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None
                })
            })
        else:
            print('is not valide', form.errors.as_data())
            client = request.POST.get('client')
            abcs= AbonnementClient.objects.filter(client=client)
            context = {'form': form}
            return render(request, self.template_name, context)

 
          
class PaiementUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required="transaction.change_paiement"
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
        messages.success(self.request, "paiement Mis a jour avec Succés")
        return HttpResponse(status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None,
                    "selected_client": f"{paiement.id}",
                })
            }) 
    
    def form_invalid(self, form):
        messages.success(self.request, form.errors )
        return self.render_to_response(self.get_context_data(form=form))   

class PaiementDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = "transaction.delete_paiement"
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
        messages.success(self.request, "Paiement Supprimer avec Succés")
        return HttpResponseRedirect(success_url)
 

#remuneration personnel ------------------------------------------------------------------------------------------
class Remuneration_Personnel(PermissionRequiredMixin,CreateView):
    permission_required = "transaction.add_remuneration"
    template_name="snippets/_remu_personnel_form.html"
    form_class=Remuneration_PersonnelModelForm

    def get_form_kwargs(self) :
        kwargs = super().get_form_kwargs()
        personnel_pk = self.kwargs.get('pk')
        if personnel_pk:
            kwargs['initial'] = {'personnel_pk': personnel_pk}
        return kwargs

    def get(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        posted_data = "\n.".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA =========\n', posted_data, '\n==========')
        
        if form.is_valid():
            print("is valide")
            form.save()
            message = _("Remuniration Personnel a été créé avec succès")
            messages.success(request, str(message))
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None
                })
            })
        else:
            print('is not valide', form.errors.as_data())
            personnel = request.POST.get("personnel")
            context = {'form': form}
            return render(request, self.template_name, context)



class RemuPersonnelUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required="transaction.change_remuneration"
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
        messages.success(self.request,"remuniration Personnel Mis a jour avec Succés")
        return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })
    def form_invalid(self, form):
        messages.success(self.request, form.errors )
        return self.render_to_response(self.get_context_data(form=form))   

class RemuPersonnelDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required="transaction.delete_remuneration"
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
        messages.success(self.request, "Remuniration Personnel Supprimer avec Succés")
        return HttpResponseRedirect(success_url)

#remuneration Coach ------------------------------------------------------------------------------------------
class Remuneration_Coach(PermissionRequiredMixin,CreateView):
    permission_required = "transaction.add_remunerationprof"
    template_name = "snippets/_remu_Coach_form.html"
    form_class = Remunération_CoachModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        coach_pk = self.kwargs.get('pk')
        if coach_pk:
            kwargs['initial'] = {'coach_pk': coach_pk}
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        posted_data = "\n.".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA =========\n', posted_data, '\n==========')
        
        if form.is_valid():
            print("is valide")
            remuneration = form.save()
            message = _("Remuniration Coach a été créé avec succès")
            messages.success(request, str(message))
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                    "refresh_table": None
                })
            })
        else:
            print('is not valide', form.errors.as_data())
            coach = request.POST.get("coach")
            context = {'form': form}
            return render(request, self.template_name, context)

    
class Remuneration_CoachUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required="transaction.change_remunerationprof"
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
        messages.success(self.request,"Remuneration Coach Mis a jour avec Succés ")
        return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None,

                })
            })
    def form_invalid(self, form):
        messages.success(self.request, form.errors )
        return self.render_to_response(self.get_context_data(form=form))   
    

class RemCoachDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required="transaction.delete_remunerationprof"
    model =RemunerationProf
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy("transactions:RemunerationProfTable_name")

    def form_valid(self,form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Remuniration Coach Supprimer avec Succés")
        return HttpResponseRedirect(success_url)

# Auter Transaction------------------------------------------------------------------------------------------
@permission_required("transaction.add_autre",raise_exception=True)
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
            messages.success(request,str(message))
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

class Autre_TransactionUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required="transaction.change_autre"
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
        form.save()
        messages.success(self.request,"Autre transactions Mis A Jour avec Succés")
        return HttpResponse(status=204,
                headers={
                    'HX-Trigger':json.dumps({
                        "closeModal":"kt_modal",
                        "refresh_table":None,

                    })
                })
    def form_invalid(self,form):
        messages.success(self.request,form.errors )
        return self.render_to_response(self.get_context_data(form=form))


class AutreTransactionDelete(PermissionRequiredMixin,DeleteView):
    permission_required="transaction.delete_autre"
    model =Autre
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy("transactions:autre_transaction_table")

    def form_valid(self,form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Autre transaction Supprimer avec Succés")
        return HttpResponseRedirect(success_url)

    


    
















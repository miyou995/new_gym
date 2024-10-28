from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import (TemplateView,UpdateView,DeleteView)
from django.shortcuts import get_object_or_404
from transaction.tables import RemunerationPersonnelHTMxTable
from presence.models import Presence, PresenceCoach
from .forms import ClientModelForm,CoachModelForm, PersonnelModelForm
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from transaction.models import Paiement, Remuneration,RemunerationProf
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .models import Client,Coach,Personnel
from .filters import ClientFilter,CoachFilter,PersonnelFilter
from .tables import (ClientHTMxTable,CoachHTMxTable,PersonnelHTMxTable,AbonnementClientHTMxTable,PaiementHTMxTable,
                     CoachDetailHTMxTable,VirementsHTMxTable,PresenceCoachHTMxTable,
                     PresenceClientHTMxTable)
from abonnement.models import AbonnementClient
from creneau.models import Creneau
from django.contrib.auth.decorators import  permission_required




#-------------------------------------------------client------------------------------------------------------------
class ClientView(PermissionRequiredMixin,SingleTableMixin, FilterView):
    permission_required = "client.view_client"
    table_class = ClientHTMxTable
    filterset_class = ClientFilter
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('from client viewwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        return context
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "client.html" 
        return template_name 

@permission_required('client.view_client', raise_exception=True)
def ClientCreateView(request):
    context = {}
    template_name = "snippets/_client_form.html"
    form = ClientModelForm(data=request.POST or None,files=request.FILES or None) 
    if request.method == "POST":
        form = ClientModelForm(data=request.POST , files=request.FILES) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            client = form.save()
            message = _("cilent a été créé avec succès.")
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
            context["form"]=ClientModelForm(data=request.POST or None )
            return render(request, template_name="snippets/_client_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)

class ClientUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required = "client.change_client"
    model = Client
    template_name="snippets/_client_form.html"
    fields=[
        "carte",
        "last_name",
        "first_name",
        "picture",
        "email",
        "adress",
        "phone",
        "civility",
        "nationality",
        "birth_date",
        "blood",
        'maladies',
        'note'
    ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        client=form.save()
        print("is from valid",client.id)
        messages.success(self.request,"Client Mis a jour avec Succés",extra_tags="toastr")
        return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })
    def form_invalid(self, form):
        messages.success(self.request, form.errors ,extra_tags="toastr")
        return self.render_to_response(self.get_context_data(form=form))   


class ClientDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = "client.delete_client"
    model =Client
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy("client:client_name")

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"] = f"Client"
        return context
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        abc= AbonnementClient.objects.filter(client=self.object)
        if abc :
            print("you can not delete this client")
            messages.error(self.request, "vous ne pouvez pas supprimer un client avec un abonnement",extra_tags="toastr")
            return HttpResponseRedirect(success_url)
        else :
            self.object.delete()
            messages.success(self.request,"Client Supprimier avec Succés",extra_tags="toastr")
            return HttpResponseRedirect(success_url)
       
#-----------------------------------------------Coach--------------------------------------------------------------
class CoachsView(PermissionRequiredMixin,SingleTableMixin,FilterView):
    permission_required = "client.view_coach"
    table_class=CoachHTMxTable
    filterset_class = CoachFilter
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_template_names(self):
        
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "coach.html" 
        return template_name 

@permission_required('client.view_coach', raise_exception=True)
def CoachCreateView(request):
    context={}
    template_name = "snippets/_coach_form.html"
    form = CoachModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = CoachModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            coach = form.save()
            message = _("Coach a été créé avec succès.")
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
            context["form"]=CoachModelForm(data=request.POST or None )
            return render(request, template_name="snippets/_coach_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)
    

class CoachUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required= "client.change_coach"
    model = Coach
    template_name="snippets/_coach_form.html"
    fields=[
       "last_name",
        "first_name",
        "email",
        "adress",
        "birth_date",
        "nationality",
        "phone",
        "civility",
        "blood",
        'color',
        'pay_per_hour',
        'note'
    ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        coach=form.save()
        print("is from valid",coach.id)
        messages.success(self.request,"Coach Mis a jour avec Succés",extra_tags="toastr")
        return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })
    def form_invalid(self, form):
        messages.success(self.request, form.errors ,extra_tags="toastr")
        return self.render_to_response(self.get_context_data(form=form)) 

class CoachDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required ="client.delete_coach"
    model= Coach
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy('client:coach_name')

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context["title"]= f"Coach"
        return context

    def form_valid(self, form):
        success_url=self.get_success_url()
        self.object.delete()
        messages.success(self.request,"Coach Supprimier avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
      
# ---------------------------------------------Personnel---------------------------------------------------------
class PersonnelsView(PermissionRequiredMixin,SingleTableMixin,FilterView):
    permission_required = "client.view_personnel"
    table_class=PersonnelHTMxTable
    filterset_class = PersonnelFilter
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_template_names(self):
        
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "personnels.html" 
        return template_name 
    
@permission_required("client.add_personnel", raise_exception=True)
def PersonnelCreateView(request):
    context={}
    template_name = "snippets/_personnels_form.html"
    form = PersonnelModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = PersonnelModelForm(data=request.POST) 
        posted_data= "\n".join(f'{key} {value}' for key, value in request.POST.items())
        print('POSTED DATA=========\n', posted_data, '\n========')
        if form.is_valid():
            print("is valide")
            coach = form.save()
            message = _("Employé a été créé avec succès.")
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
            context["form"]=PersonnelModelForm(data=request.POST or None )
            return render(request, template_name="snippets/_personnels_form.html", context=context)
    context["form"] = form
    return render(request, template_name=template_name, context=context)
    
class PersonnelUpdateView(PermissionRequiredMixin,UpdateView):
    permission_required  = "client.change_personnel"
    model = Personnel
    template_name="snippets/_personnels_form.html"
    fields=[
        "last_name",
        "first_name",
        "function",
        "adress",
        "birth_date",
        "nationality",
        "phone",
        "civility",
        "blood",
        "state",
        'note'
    ]
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        print('form instance',self.object)
        return super().get(request,*args, **kwargs)
    def form_valid(self,form):
        personnel=form.save()
        print("is from valid",personnel.id)
        messages.success(self.request,"Personnel Mis a jour avec Succés",extra_tags="toastr")
        return HttpResponse(status=204,
            headers={
                "HX-Trigger":json.dumps({
                    "closeModal":"kt_modal",
                    "refresh_table":None
                })
            })
    def form_invalid(self, form):
        messages.success(self.request, form.errors ,extra_tags="toastr")
        return self.render_to_response(self.get_context_data(form=form)) 

class PersonnelDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = "client.delete_personnel"
    model= Personnel
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy('client:personnels_name')

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context["title"]= f"Employé"
        return context

    def form_valid(self, form):
        success_url=self.get_success_url()
        self.object.delete()
        messages.success(self.request,"Employé Supprimier avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    


# ----------------------------------------------client detail-----------------------------------------
class AbonnementClientDetail(SingleTableMixin, FilterView):
    table_class =   AbonnementClientHTMxTable
    paginate_by = 15
    model = AbonnementClient

    def get_queryset(self):
         queryset = AbonnementClient.objects.select_related('client', "type_abonnement").order_by("-created_date_time")
         abonnement_client_pk = self.kwargs.get('pk')
         print("abonnement_client_pk from abc -------------", abonnement_client_pk)
         if abonnement_client_pk:
            queryset = queryset.filter(client_id=abonnement_client_pk)
         return queryset
    
    def get_context_data(self, **kwargs):
        context = super(AbonnementClientDetail, self).get_context_data(**kwargs)
        context["client"] = Client.objects.get(pk=self.kwargs['pk'])
        print('context abc ------****************---------->>>>>')

        # context["abc"] = self.kwargs['pk']
        # print('context abc ---------------->>>>>',context['abc'])
        return context
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "snippets/client_detail.html"
        return template_name
    

class PaiementClientDetail(SingleTableMixin, FilterView):
        table_class =   PaiementHTMxTable
        paginate_by = 15
        model = Paiement
        
        def get_queryset(self):
            queryset = Paiement.objects.order_by("-date_creation")
            abonnement_client_pk = self.kwargs.get('pk')
            print("abonnement_client_pk  -------------", abonnement_client_pk)
            if abonnement_client_pk:
                queryset = queryset.filter(abonnement_client__client=abonnement_client_pk)
                return queryset
        
        def get_template_names(self):
            if self.request.htmx:
                template_name = "tables/product_table_partial.html"
            else:
                template_name = "snippets/client_detail.html"
            return template_name

class PresenceClientDetail(SingleTableMixin, FilterView):
        table_class =   PresenceClientHTMxTable
        paginate_by = 15
        model = Presence
        
        def get_queryset(self):
            queryset = Presence.objects.order_by("-created")
            abonnement_client_pk = self.kwargs.get('pk')
            print("abonnement_client_pk from presence -------------", abonnement_client_pk)
            if abonnement_client_pk:
                queryset = queryset.filter(abc__client=abonnement_client_pk)
                return queryset
        
        def get_template_names(self):
            if self.request.htmx:
                template_name = "tables/product_table_partial.html"
            else:
                template_name = "snippets/client_detail.html"
            return template_name




# ----------------------------------------coach detail --------------------------------------------------
class CoachDetail(SingleTableMixin, FilterView):
    table_class =   CoachDetailHTMxTable
    paginate_by = 15
    model = Creneau

    def get_context_data(self, **kwargs):
        context = super(CoachDetail, self).get_context_data(**kwargs)
        context["coach"] =  Coach.objects.get(pk=self.kwargs['pk'])

        return context
    
    def get_queryset(self):
         queryset = Creneau.objects.select_related('coach').order_by("-created")
         coach_pk = self.kwargs.get('pk')
         print("coach_pk -------------", coach_pk)
         if coach_pk:
            queryset = queryset.filter(coach_id=coach_pk)

         return queryset
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "snippets/coach_detail.html"
        return template_name
    
class VirementsCoachDetail(SingleTableMixin, FilterView):
    table_class =   VirementsHTMxTable
    paginate_by = 15
    model = RemunerationProf
    
    def get_queryset(self):
         queryset = RemunerationProf.objects.order_by("-date_creation")
         coach_pk = self.kwargs.get('pk')
         print("coach_pk virements  -------------", coach_pk)
         if coach_pk:
            queryset = queryset.filter(coach_id=coach_pk)

         return queryset
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "snippets/coach_detail.html"
        return template_name

class PresenceCoachDetail(SingleTableMixin, FilterView):
    table_class =   PresenceCoachHTMxTable
    paginate_by = 15
    model = PresenceCoach
    
    def get_queryset(self):
         queryset = PresenceCoach.objects.order_by("-date")
         coach_pk = self.kwargs.get('pk')
         print("coach_pk presences -------------", coach_pk)
         if coach_pk:
            queryset = queryset.filter(coach_id=coach_pk)
            print("quey-----------------",queryset)
         return queryset
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "snippets/coach_detail.html"
        return template_name
    

def presence_coach(request, pk):
    context={}
    coach_pk = get_object_or_404(Coach, pk=pk)
    print("coach_pk enter ------------------------", coach_pk)
    in_salle=coach_pk.enter_sotrie_coach()
    print("is_salle from view*****************************",in_salle)
    presnce =PresenceCoach.objects.filter(coach=in_salle).first()
    
    print('presnece view///////////////////////////',presnce)
    context["presence"]=presnce
    if in_salle :
        messages.success(request, "Entrée /Sorté Coach Enregistrée", extra_tags="toastr")
    else :
        messages.error(request, "Coach ",extra_tags="toastr")
    return HttpResponse(status=204)


# ----------------------------------------Personnel detail --------------------------------------------------


class PersonnelDetail(SingleTableMixin, FilterView):
    table_class =   RemunerationPersonnelHTMxTable
    paginate_by = 15
    model = Remuneration

    def get_context_data(self, **kwargs):
        context = super(PersonnelDetail, self).get_context_data(**kwargs)
        context["personnel"] =  Personnel.objects.get(pk=self.kwargs['pk'])

        return context
    
    def get_queryset(self):
         queryset = Remuneration.objects.select_related('nom').order_by("-date_creation")
         personnel_pk = self.kwargs.get('pk')
         print("personnel_pk -------------", personnel_pk)
         if personnel_pk:
            queryset = queryset.filter(nom_id=personnel_pk)

         return queryset
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "snippets/personnel_detail.html"
        return template_name



    

    




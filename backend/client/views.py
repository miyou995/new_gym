from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import (TemplateView,UpdateView,DeleteView)
from .forms import ClientModelForm,CoachModelForm, PersonnelModelForm
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.urls import reverse_lazy

from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .models import Client,Coach,Personnel
from .filters import ClientFilter,CoachFilter,PersonnelFilter
from .tables import ClientHTMxTable,CoachHTMxTable,PersonnelHTMxTable


#  tables views
class ClientView(SingleTableMixin, FilterView):
    table_class = ClientHTMxTable
    filterset_class = ClientFilter
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      
        return context
    def get_template_names(self):
        
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "client.html" 
        return template_name 
    


class CoachsView(SingleTableMixin,FilterView):
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


class PersonnelsView(SingleTableMixin,FilterView):
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


def ClientCreateView(request):
    context = {}
    template_name = "snippets/_client_form.html"
    form = ClientModelForm(data=request.POST or None) 
    if request.method == "POST":
        form = ClientModelForm(data=request.POST) 
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


class ClientUpdateView(UpdateView):
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
        messages.success(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))   


class ClientDeleteView(DeleteView):
    model =Client
    template_name="snippets/delete_modal.html"
    success_url=reverse_lazy("client:client_name")

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["title"] = f"Client"
        return context
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request,"Client Supprimier avec Succés",extra_tags="toastr")
        return HttpResponseRedirect(success_url)
    



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
    


class CoachUpdateView(UpdateView):
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
        messages.success(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form)) 



class CoachDeleteView(DeleteView):
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
    


class PersonnelUpdateView(UpdateView):
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
        messages.success(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form)) 



class PersonnelDeleteView(DeleteView):
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
    






class ClientDetailView(TemplateView):
    template_name = "snippets/client_detail.html"

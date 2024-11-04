from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import FormView
from django.views.generic import UpdateView, ListView, TemplateView,DetailView,DeleteView
from .models import User
from django.contrib.auth.models import  Permission , Group
from django.contrib.auth.decorators import  permission_required
from django.views import View
import json
from django_htmx.http import HttpResponseClientRedirect
from django.http import HttpResponse, HttpResponseRedirect
from .froms import (UserCreationForm, UserEditionForm, 
ChangePasswordForm,AddGroupForm)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
import logging
from django.contrib.admin.views.main import ChangeList
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login
from .utils import get_permissions
from django.contrib.auth.views import LoginView

logger = logging.getLogger(__name__)


# -----------------------------LOGIN--LOGOUT----------------------------------------------------------

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('core:index'))
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        user = self.request.user 
        if not user:
            messages.error(self.request, _("Email ou mot de passe incorrect."), extra_tags="toastr")
            return "/"
        redirect_url = redirect('/')
        return reverse('accounts:userdetail', kwargs={'pk': user.pk})
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, _("Invalid credentials."), extra_tags="toastr")
        return self.render_to_response(self.get_context_data(form=form))
    

def logout_view(request):
    logout(request)
    return redirect('/')

# -----------------------------------USER VIEWS----------------------------------------------------

class UserCreateView(PermissionRequiredMixin, FormView):
    permission_required = 'accounts.add_user'
    template_name = "accounts/snippets/create_user.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        new_user = form.save()
        messages.success(self.request, _("Account Created successfully"), extra_tags="toastr")
        print('new_user>>>>>> ID', new_user.pk)
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "closeModal": "kt_modal",
                })
            }
        )
    def form_invalid(self, form):
        messages.error(self.request, form.errors , extra_tags="toastr")
        return self.render_to_response(self.get_context_data(form=form)) 


class UserUpdateView(PermissionRequiredMixin, View):
    permission_required = 'accounts.change_user'
    template_name = "accounts/snippets/create_user.html"

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = UserEditionForm(instance=user)
        context = {"form": form, "user": user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = UserEditionForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Account Updated successfully") , extra_tags="toastr")
            return HttpResponse(status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": "kt_modal",
                    })
                })   
        
        else:
            messages.error(request, form.errors , extra_tags="toastr")
            return render(request, self.template_name, {'form': form, 'user': user})



class UserDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required='account:delete_user'
    model = User
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("accounts:userlist")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "User Supprimer avec Succés" , extra_tags="toastr")
        return HttpResponseRedirect(success_url)


class UserDetailView(DetailView):
    model = User
    context_object_name = "user"
    template_name= "accounts/user-detail.html"
    def get_context_data(self, *args,**kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["user_permissions"] = self.get_object().user_permissions.all()
        print('user groups', self.object.groups.all())
        context["user_groups"] = self.object.groups.all()  

        context['permissions']= get_permissions()
        # print('permssios ns>>>>>>>>>>', self.get_object().user_permissions.all())
        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        perms = request.POST.getlist('perms')
        permissions = Permission.objects.filter(id__in=perms)
        user.user_permissions.set(permissions)
        user.save()
        messages.success(request, _('Profile updated successfully') , extra_tags="toastr")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'accounts.view_user'
    template_name = 'accounts/user_list.html' 
    success_url = reverse_lazy('accounts:userlist')
    context_object_name= "users"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context["permissions"] = Permission.objects.all()
        context["user_groups"] = Group.objects.all()
        return context 
        

@permission_required('accounts.change_user', raise_exception=True)
def change_password(request, pk):
    context= {}
    template_name="accounts\snippets\change_password.html"
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = ChangePasswordForm(request.POST ,instance=user)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            password = cd['password']
            password2 = cd['password2']
            if password == password2:
                user.set_password(password)
                user.save()
                messages.success(request, _('Mot de passe modifié avec succès'),extra_tags="toastr")
                redirect_url = reverse("accounts:userlist")
                return HttpResponseClientRedirect(redirect_url)
            else:
                messages.error(request, _('Formulaire invalide'), extra_tags="toastr")
        else:
            messages.error(request, _('Formulaire invalide'),extra_tags="toastr")
            context["form"]=ChangePasswordForm(data=request.POST or None )
            return render(request, template_name="accounts\snippets\change_password.html", context=context)
    else:
        user_form = ChangePasswordForm()  
    context = {'form': user_form, 'user': user}
    return render(request, template_name, context)





#-----------------------------------------groupe--------------------------------------------------------


#### CREATE  |  #### EDIT
@permission_required(('auth.add_group','auth.change_group'), raise_exception=True)
def add_edit_group(request, pk=None):
    context = {}
    context['page_title'] = _("Roles")
    role=None
    if pk:
        role = get_object_or_404(Group.objects.prefetch_related('permissions'), pk=pk)
    form  =  AddGroupForm( instance=role,)
    if request.method == "POST":
        form  =  AddGroupForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            message = _("Role created successfully")
            messages.success(request, str(message), extra_tags="toastr" )
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": "kt_modal",
                        "refresh_table": None,
                    })
                }
            )
        else:
            messages.error(request, form.errors , extra_tags="toastr"  )
            print("is not valide", form.errors.as_data())
    
    context["form"] = form 
    context["role"]= role
    context ["permissions"] = get_permissions()
    return render(request, 'accounts/snippets/create_edit_group_form.html', context)



class GroupListView(PermissionRequiredMixin, ListView):
    model = Group
    permission_required = 'accounts.view_group'
    template_name = 'accounts/group_list.html' 
    success_url = reverse_lazy('accounts:grouplist')
    context_object_name= "roles"

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context["permissions"] = Permission.objects.all()

        return context 



class GroupDetailView(PermissionRequiredMixin, DetailView):
    model = Group
    permission_required = 'auth.view_group'
    template_name = "/role/_role_detail.html" 
    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        group = self.object
        context["staff"] = User.objects.filter(groups__id=group.id)
        context["page_title"]= _("Role details")
        context["parent_page"]= _('Users')
        context["parent_url"]= reverse('accounts:user_management')
        return context




class GroupDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required='auth.delete_group'
    model = Group
    template_name = "buttons/delete.html"
    success_url = reverse_lazy("accounts:grouplist")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_url"] = reverse('accounts:delete_group', kwargs={'pk': str(self.object.id)}) 
        return context
    





# -----------------------------------SignupView---------------------------------------------------------
    
class SignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:signup_success')
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        return response    

class SignupsuccessView(TemplateView):
    template_name = "accounts/signup_message.html" 
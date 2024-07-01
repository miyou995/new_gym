
from django.shortcuts import render
from .models import AbonnementClient

# Create your views here.

def abc_htmx_view(request):
    client_id = request.GET.get('client')
    template_name = "abc_hx.html"
    abcs=AbonnementClient.objects.filter(client__id=client_id)
    return render(request, template_name, {'abcs': abcs})

from django.utils.translation import gettext as _
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

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
        return reverse('core:index')
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, _("Invalid credentials."), extra_tags="toastr")
        return self.render_to_response(self.get_context_data(form=form))
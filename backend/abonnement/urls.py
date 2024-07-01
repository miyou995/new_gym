from django.urls import path, include
from .views import (
                    abc_htmx_view
)
from .forms import AuthenticationForm
# , RenewalSubscription
from .views import *
app_name = 'abonnement'


urlpatterns = [

    path('abc_htmx_view/', abc_htmx_view, name='abc_htmx_view'),
    path('login/', CustomLoginView.as_view(
        template_name="accounts/login.html",
        form_class=AuthenticationForm,
    ), name='login'),







]



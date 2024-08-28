from django.urls import path, include
from .views import (
                    abc_htmx_view,CreateAbonnemtClient
)
# , RenewalSubscription
from .views import *
app_name = 'abonnement'


urlpatterns = [

    path('abc_htmx_view/', abc_htmx_view, name='abc_htmx_view'),
    path('CreateAbonnemtClient/<str:pk>', CreateAbonnemtClient.as_view(), name='create_abonnement_client'),








]



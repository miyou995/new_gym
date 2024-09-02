from django.urls import path
from .views import (
                    abc_htmx_view,CalendarAbonnementClient
)
# , RenewalSubscription
from .views import *
app_name = 'abonnement'


urlpatterns = [

    path('abc_htmx_view/', abc_htmx_view, name='abc_htmx_view'),
    path('calendar_abonnement_client/<str:pk>', CalendarAbonnementClient.as_view(), name='calendar_abonnement_client'),








]



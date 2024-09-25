from django.urls import path
from .views import (
                    abc_htmx_view,CalendarAbonnementClient,add_abonnement_client,update_abonnement_client
)
# , RenewalSubscription
from .views import *
app_name = 'abonnement'


urlpatterns = [

    path('abc_htmx_view/', abc_htmx_view, name='abc_htmx_view'),
    path('calendar_abonnement_client/<str:pk>', CalendarAbonnementClient.as_view(), name='calendar_abonnement_client'),
    path('add_abonnement_client/<str:client_pk>/<str:type_abonnement>', add_abonnement_client, name='add_abonnement_client'),




    path('CalendarUpdateAbonnementClient/<str:pk>', CalendarUpdateAbonnementClient.as_view(), name='calendar_update_abonnementclient'),
    path('update_abonnement_client/<int:pk>/<str:type_abonnement>', update_abonnement_client, name='update_abonnement_client'),
    path('abonnemt_client_delete/<int:pk>', AbonnemtClientDeleteView.as_view(), name='abonnemt_client_delete'),







]



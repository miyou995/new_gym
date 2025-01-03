from django.urls import path
from .views import (
                    abc_htmx_view,CalendarAbonnementClient,add_abonnement_client,update_abonnement_client,
                    update_date_paiement_rest,renew_abonnement_client,block_deblock_abonnement_client
)
# , RenewalSubscription
from .views import *
app_name = 'abonnement'


urlpatterns = [

    path('abc_htmx_view/', abc_htmx_view, name='abc_htmx_view'),
    path('calendar_abonnement_client/<str:pk>', CalendarAbonnementClient.as_view(), name='calendar_abonnement_client'),
    path('add_abonnement_client/<str:client_pk>/<str:type_abonnement>', add_abonnement_client, name='add_abonnement_client'),


    path('retreive_abc/<str:pk>', RetreiveAbonnementClient.as_view(), name='retreive_abc'),
    path('update_abonnement_client/<int:pk>', update_abonnement_client, name='update_abonnement_client'),

    path('abonnemt_client_delete/<int:pk>', AbonnemtClientDeleteView.as_view(), name='abonnemt_client_delete'),
    
    path('update_date_paiement_rest/<int:pk>/', update_date_paiement_rest, name='update_date_paiement_rest'),
    path('renew_abonnement_client/<int:pk>/', renew_abonnement_client, name='renew_abonnement_client'),
    path('block_deblock_abonnement_client/<int:pk>/', block_deblock_abonnement_client, name='block_deblock_abonnement_client'),

]



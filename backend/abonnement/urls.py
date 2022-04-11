from django.urls import path, include
from .views import AbonnementAPIView, AbonnementListAPIView, AbonnementDetailAPIView, AbonnementDestroyAPIView ,AbonnementClientCreateAPIView ,AbonnementClientListAPIView ,AbonnementClientDetailAPIView ,AbonnementClientDestroyAPIView, renew_api_view, AbonnementClientDetailListApi, AbonnementClientTransactionsDetailListApi, total_dettes_abonnee, deactivate_api_view,deactivate_abc_api_view, ABClientByCreneauListAPIView, total_restes_abonnees
# , RenewalSubscription
from .views import *
app_name = 'abonnement'


urlpatterns = [
    path('abonnement/', AbonnementListAPIView.as_view(),  name="abonnement"),
    path('abonnement/<int:pk>/', AbonnementDetailAPIView.as_view(), name="abonnement-delete"),
    path('abonnement/create', AbonnementAPIView.as_view(),  name="abonnement-create"),
    path('abc-by-creneau', ABClientByCreneauListAPIView.as_view(),  name="abonnement-by-creneau"),
    path('abonnement/delete/<int:pk>/', AbonnementDestroyAPIView.as_view(), name="abonnement-delete"),
    path('abonnement/deativate/<int:pk>/', deactivate_api_view, name="abonnement-delete"),
    path('abonnement-client/deativate/<int:pk>/', deactivate_abc_api_view, name="abonnement-delete"),

    path('abonnement-client/', AbonnementClientListAPIView.as_view(),  name="type"),
    path('abonnement-client-dettes/', total_dettes_abonnee,  name="abonnement-client-dettes"),
    path('totales-restes/', total_restes_abonnees,  name="totales-restes"),
    path('abonnement-transactions/', AbonnementClientTransactionsDetailListApi.as_view(),  name="transactions"),
    path('abonnement-by-client/', AbonnementClientDetailListApi.as_view(),  name="abc-by-client"),
    path('abonnement-client/renew/<int:pk>/', renew_api_view, name="type-delete"),
    path('abonnement-client/<int:pk>/', AbonnementClientDetailAPIView.as_view(), name="type-delete"),
    path('abonnement-client/create', AbonnementClientCreateAPIView.as_view(),  name="type-create"),
    path('abonnement-client/delete/<int:pk>/', AbonnementClientDestroyAPIView.as_view(), name="type-delete"),
]



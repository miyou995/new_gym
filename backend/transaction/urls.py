
from django.urls import path
from .views import (
                    TransactionView,chiffre_affaire,Remuneration_Personnel,paiement,Remuneration_Coach,Autre_Transaction,
                    PaiementUpdateView,RemunerationProfTable,
                    RemunerationPersonnelTable,PaiementDeleteView,RemuPersonnelUpdateView,Remuneration_CoachUpdateView,RemuPersonnelDeleteView,RemCoachDeleteView,
                    AutreTransactionTable,Autre_TransactionUpdateView,AutreTransactionDelete,
                    chiffre_par_abonnement,chiffre_par_Activity,chifre_dattes_abonnement,impression_resu_paiement)

app_name = 'transactions'


urlpatterns = [

        path('chiffre_affaire/',chiffre_affaire.as_view(), name='chiffre_affaire_name'),
        path('chiffre_par_abonnement/',chiffre_par_abonnement, name='chiffre_par_abonnement_name'),
        path('chiffre_par_Activity/',chiffre_par_Activity, name='chiffre_par_Activity_name'),
        path('chifre_dattes_abonnement/',chifre_dattes_abonnement, name='chifre_dattes_abonnement_name'),

        path('transaction/',TransactionView.as_view(), name='transaction_name'),
        path('transaction/paiement_name',paiement.as_view(), name='paiement_name'),
        path('transaction/paiement_name/<str:pk>',paiement.as_view(), name='client_paiement_name'),

        path('transaction/remuneration_personnel_name',Remuneration_Personnel.as_view(), name='remuneration_personnel_name'), 
        path('transaction/remuneration_personnel_detail/<str:pk>',Remuneration_Personnel.as_view(), name='remuneration_personnel_detail'), 

        path('transaction/remuneration_coach_name',Remuneration_Coach.as_view(), name='remuneration_coach_name'),
        path('transaction/coach_remuneration_coach/<int:pk>',Remuneration_Coach.as_view(), name='coach_remuneration_coach'),  
        path('transaction/autre_transaction_name',Autre_Transaction, name='autre_transaction_name'), 

        # updateView
        path("transaction/paiement_update/<int:pk>", PaiementUpdateView.as_view(), name="paiement_update"),
        path("transaction/remuneration_personnel_update/<int:pk>", RemuPersonnelUpdateView.as_view(), name="remuneration_personnel_update"),
        path("transaction/remuneration_coach_update/<int:pk>", Remuneration_CoachUpdateView.as_view(), name="remuneration_coach_update"),
        path("transaction/autre_transaction_update/<int:pk>", Autre_TransactionUpdateView.as_view(), name="autre_transaction_update"),


        path('transaction/remuneration_prof_table_name',RemunerationProfTable.as_view(), name='remuneration_prof_table_name'),
        path('transaction/remuneration_personnel_table_name',RemunerationPersonnelTable.as_view(), name='remuneration_personnel_table_name'),
        path('transaction/autre_transaction_table',AutreTransactionTable.as_view(), name='autre_transaction_table'),

      
#       deleteview
        path("transaction/paiement_delete_view_name/<int:pk>", PaiementDeleteView.as_view(), name="paiement_delete_view_name"),
        path("transaction/remu_personnel_delete_view_name/<int:pk>", RemuPersonnelDeleteView.as_view(), name="remu_personnel_delete_view_name"),
        path("transaction/rem_coach_delete_view_name/<int:pk>", RemCoachDeleteView.as_view(), name="rem_coach_delete_view_name"),
        path("transaction/autre_transaction_delete/<int:pk>", AutreTransactionDelete.as_view(), name="autre_transaction_delete"),

        path('impression_resu_paiement/<int:paiement_id>/', impression_resu_paiement, name='impression_resu_paiement'),



       



]



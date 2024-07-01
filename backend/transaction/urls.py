
from django.urls import path, include
from .views import (
                    TransactionView,Chiffre_affaireView,Remuneration_Personnel,paiement,Remuneration_Coach,Autre_Transaction,
                    PaiementUpdateView,RemunerationProfTable,
                    RemunerationPersonnelTable,PaiementDeleteView,RemuPersonnelUpdateView,Remuneration_CoachUpdateView,RemuPersonnelDeleteView,RemCoachDeleteView)
# RemunerationEmployeListAPIView, RemunerationEmployeDetailAPIView, RemunerationEmployeAPIView, PaiementEmployeListAPIView

app_name = 'transactions'


urlpatterns = [

        path('transaction/',TransactionView.as_view(), name='transaction_name'),
        path('chiffre_affaire/',Chiffre_affaireView.as_view(), name='chiffre_affaire_name'),
        path('transaction/paiement_name',paiement, name='paiement_name'),
        path('transaction/Remuneration_Personnel',Remuneration_Personnel, name='Remuneration_Personnel_name'), 
        path('transaction/Remuneration_Coach',Remuneration_Coach, name='Remuneration_Coach_name'), 
        path('transaction/Autre_Transaction',Autre_Transaction, name='Autre_Transaction_name'), 

        # updateView
        path("transaction/update/<int:pk>", PaiementUpdateView.as_view(), name="paiement_update"),
        path("transaction/Remuneration_Personnel/update/<int:pk>", RemuPersonnelUpdateView.as_view(), name="Remuneration_Personnel_update"),
        path("transaction/Remuneration_Coach/update/<int:pk>", Remuneration_CoachUpdateView.as_view(), name="Remuneration_Coach_update"),


        path('transaction/RemunerationProfTable',RemunerationProfTable.as_view(), name='RemunerationProfTable_name'),
        path('transaction/RemunerationPersonnelTable',RemunerationPersonnelTable.as_view(), name='RemunerationPersonnelTable_name'),

      
#       deleteview
        path("transaction/delete/<int:pk>", PaiementDeleteView.as_view(), name="PaiementDeleteView_name"),
        path("transaction/Remuneration_Personnel/delete/<int:pk>", RemuPersonnelDeleteView.as_view(), name="RemuPersonnelDeleteView_name"),
        path("transaction/Remuneration_Coach/delete/<int:pk>", RemCoachDeleteView.as_view(), name="RemCoachDeleteView_name"),


        # path('transaction/ProductHTMxTableView',ProductHTMxTableView.as_view(), name='product_htmx'), 
       



]



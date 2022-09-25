from django.urls import path, include
from .views import PaiementAPIView, PaiementListAPIView, PaiementDetailAPIView, PaiementDestroyAPIView, AutreAPIView, AutreListAPIView, AutreDetailAPIView, AutreDestroyAPIView, AssuranceAPIView, AssuranceListAPIView, AssuranceDetailAPIView, AssuranceDestroyAPIView, RemunerationAPIView, RemunerationListAPIView, RemunerationDetailAPIView, RemunerationDestroyAPIView, RemunerationProfAPIView, RemunerationProfListAPIView, RemunerationProfDetailAPIView, RemunerationProfDestroyAPIView, TransactionListAPIView, TransactionDetailAPIView, PaiementCoachListAPIView, total_charges, chiffre_affaire,  TransToday, PaiementClientListAPIView, ca_by_salle, ca_by_ab, MyModelViewSet, ca_by_date, PaiementEmployeListAPIView, PaiementHistoryListAPIView, get_transaction_authorization
# RemunerationEmployeListAPIView, RemunerationEmployeDetailAPIView, RemunerationEmployeAPIView, PaiementEmployeListAPIView

app_name = 'transactions'


urlpatterns = [
    path('', TransactionListAPIView.as_view(),  name="transaction"),
    # path('detail/<int:pk>/', TransactionDetailAPIView.as_view(),  name="transaction-detail"),
    path('paiement/create', PaiementAPIView.as_view(),  name="paiement-create"),
    path('paiement/', PaiementListAPIView.as_view(),  name="paiement"),
    path('paiement/', PaiementListAPIView.as_view(),  name="paiement"),
    path('paiement/by_test', MyModelViewSet.as_view(),  name="paiement"),
    path('paiement/ca-by-salle', ca_by_salle,  name="ca-by-filters"),
    path('paiement/ca-by-abonnement', ca_by_ab,  name="ca-by-filters"),
    # path('paiement/ca-by-activity', ca_by_activity,  name="ca-by-filters"),
    path('paiement-by-client/', PaiementClientListAPIView.as_view(),  name="paiement"),
    path('paiement/<int:pk>/', PaiementDetailAPIView.as_view(), name="paiement-delete"),
    path('paiement/delete/<int:pk>/', PaiementDestroyAPIView.as_view(), name="paiement-delete"),
    path('paiement/history/', PaiementHistoryListAPIView.as_view(),  name="paiement-history"),

    path('autre/create', AutreAPIView.as_view(),  name="autre-create"),
    path('autre/', AutreListAPIView.as_view(),  name="autre"),
    path('autre/<int:pk>/', AutreDetailAPIView.as_view(), name="autre-delete"),
    path('autre/delete/<int:pk>/', AutreDestroyAPIView.as_view(), name="autre-delete"),

    path('assurance/create', AssuranceAPIView.as_view(),  name="assurance-create"),
    path('assurance/', AssuranceListAPIView.as_view(),  name="assurance"),
    path('assurance/<int:pk>/', AssuranceDetailAPIView.as_view(), name="assurance-delete"),
    path('assurance/delete/<int:pk>/', AssuranceDestroyAPIView.as_view(), name="assurance-delete"),

    path('remuneration/create', RemunerationAPIView.as_view(),  name="remuneration-create"),
    path('remuneration/', RemunerationListAPIView.as_view(),  name="remuneration"),
    # path('remunerationProf-by-coach/', PaiementEmployeListAPIView.as_view(),  name="remunerationProf-create"),
    path('remuneration/<int:pk>/', RemunerationDetailAPIView.as_view(), name="remuneration-delete"),
    path('remuneration/delete/<int:pk>/', RemunerationDestroyAPIView.as_view(), name="remuneration-delete"),
    path('get_transaction_authorization/', get_transaction_authorization, name="get_transaction_authorization"),


    # path('remunerationProf/', RemunerationEmployeListAPIView.as_view(),  name="remunerationEmploye"),
    # path('remunerationEmploye/<int:pk>/', RemunerationEmployeDetailAPIView.as_view(), name="remunerationEmploye-delete"),
    # path('remunerationEmploye/create', RemunerationEmployeAPIView.as_view(),  name="remunerationEmploye-create"),
    # path('remunerationEmploye-by-coach/', PaiementEmployeListAPIView.as_view(),  name="remunerationEmploye-create"),

    path('remunerationProf/', RemunerationProfListAPIView.as_view(),  name="remunerationProf"),
    path('remunerationProf/<int:pk>/', RemunerationProfDetailAPIView.as_view(), name="remunerationProf-delete"),
    path('remunerationProf/create', RemunerationProfAPIView.as_view(),  name="remunerationProf-create"),
    path('remunerationProf-by-coach/', PaiementCoachListAPIView.as_view(),  name="remunerationProf-create"),
    path('remunerationProf/delete/<int:pk>/', RemunerationProfDestroyAPIView.as_view(), name="remunerationProf-delete"),
    path('total-charges/', total_charges, name="total-charges"),
    path('chiffre-affaire/', chiffre_affaire, name="chiffre-affaire"),
    path('ca_by_date', ca_by_date, name="ca_by_date"),
    # path('trans-today/', trans_today, name="trans-today"),
    
    path('trans-today/', TransToday.as_view(), name="trans-today"),
]



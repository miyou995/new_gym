
from django.urls import path
from .views import (IndexView,PlanningTable,SalleTable ,ActivityTable,MaladieTable,PortesTable,AbonnementTable,
                    PlanningCreateView,PlanningUpdateView,PlanningDeleteView,SalleCreateView,SalleUpdateView
                    ,SalleDeleteView,ActiviteCreateView,ActiviteUpdateView,ActiviteDeleteView,MaladieCreateView,
                   MaladieUpdateView,MaladieDeleteView,PorteCreateView,PorteUpdateView,
                   PorteDeleteView,TypeAbonnementCreateView,TypeAbonnementUpdateView,TypeAbonnementDeleteView,
                  )



app_name= 'core'


urlpatterns = [
    path("", IndexView.as_view(), name="index"), 
    # path("actuellement_en_salle/", ActuellementEnSalle.as_view(), name="actuellement_en_salle"), 
    

    # path('configuration/',ConfigurationView.as_view(), name='configuration_name'),
    path('configuration/', PlanningTable.as_view(), name='planning_table'),
    path('configuration/SalleTable',SalleTable.as_view(), name='SalleTable'),
    path('configuration/ActivityTable',ActivityTable.as_view(), name='ActivityTable'),
    path('configuration/MaladieTable',MaladieTable.as_view(), name='MaladieTable'),
    path('configuration/PortesTable', PortesTable.as_view(), name='PortesTable'),
    path('configuration/AbonnementTable', AbonnementTable.as_view(), name='AbonnementTable'),

    
    
# planning--------------------------------------------------------------------------------------
    path('configuration/PlanningCreateView', PlanningCreateView, name='PlanningCreateView'),
    path('configuration/PlanningCreateView/<str:pk>',PlanningUpdateView.as_view(),name="PlanningUpdateView"),
    path("configuration/PlanningDeleteView/<int:pk>", PlanningDeleteView.as_view(), name="PlanningDeleteView"),

# salle----------------------------------------------------------------------------------------------
    path('configuration/SalleCreateView', SalleCreateView, name='SalleCreateView'),
    path('configuration/SalleUpdateView/<str:pk>',SalleUpdateView.as_view(),name="SalleUpdateView"),
    path("configuration/SalleDeleteView/<int:pk>",SalleDeleteView.as_view(), name="SalleDeleteView"),
    
# Activites------------------------------------------------------------------------------------------
    path('configuration/ActiviteCreateView', ActiviteCreateView, name='ActiviteCreateView'),
    path('configuration/ActiviteUpdateView/<str:pk>',ActiviteUpdateView.as_view(),name="ActiviteUpdateView"),
    path("configuration/ActiviteDeleteView/<int:pk>", ActiviteDeleteView.as_view(), name="ActiviteDeleteView"),

# Maladie--------------------------------------------------------------------------------------------
    path('configuration/MaladieCreateView', MaladieCreateView, name='MaladieCreateView'),
    path('configuration/MaladieUpdateView/<str:pk>',MaladieUpdateView.as_view(),name="MaladieUpdateView"),
    path("configuration/MaladieDeleteView/<int:pk>", MaladieDeleteView.as_view(), name="MaladieDeleteView"),

#Portes--------------------------------------------------------------------------------------------------
    path('configuration/PorteCreateView', PorteCreateView, name='PorteCreateView'),
    path('configuration/PorteUpdateView/<str:pk>',PorteUpdateView.as_view(),name="PorteUpdateView"),
    path("configuration/PorteDeleteView/<int:pk>", PorteDeleteView.as_view(), name="PorteDeleteView"),

# Abonnement-------------------------------------------------------------------------------------------------
    path('configuration/TypeAbonnementCreateView', TypeAbonnementCreateView, name='TypeAbonnementCreateView'),
    path('configuration/TypeAbonnementUpdateView/<str:pk>',TypeAbonnementUpdateView.as_view(),name="TypeAbonnementUpdateView"),
    path("configuration/TypeAbonnementDeleteView/<int:pk>", TypeAbonnementDeleteView.as_view(), name="TypeAbonnementDeleteView"),


    

   

]






from django.urls import path
from .views import (IndexView,PlanningTable,SalleTable ,ActivityTable,MaladieTable,PortesTable,AbonnementTable,
                    planning_create_view,PlanningUpdateView,PlanningDeleteView,salle_create_view,SalleUpdateView
                    ,SalleDeleteView,activite_create_view,ActiviteUpdateView,ActiviteDeleteView,maladie_create_view,
                   MaladieUpdateView,MaladieDeleteView,porte_create_view,PorteUpdateView,
                   PorteDeleteView,type_abonnement_create_view,TypeAbonnementUpdateView,TypeAbonnementDeleteView,
                  open_salle,close_salle)



app_name= 'core'


urlpatterns = [
    path("", IndexView.as_view(), name="index"), 
    # path("actuellement_en_salle/", ActuellementEnSalle.as_view(), name="actuellement_en_salle"), 
    

    # path('configuration/',ConfigurationView.as_view(), name='configuration_name'),
    path('configuration/', PlanningTable.as_view(), name='planning_table'),
    path('configuration/salle_table',SalleTable.as_view(), name='salle_table'),
    path('configuration/activity_table',ActivityTable.as_view(), name='activity_table'),
    path('configuration/maladie_table',MaladieTable.as_view(), name='maladie_table'),
    path('configuration/portes_table', PortesTable.as_view(), name='portes_table'),
    path('configuration/abonnemen_table', AbonnementTable.as_view(), name='abonnemen_table'),

    
    
# planning--------------------------------------------------------------------------------------
    path('configuration/planning_create_view', planning_create_view, name='planning_create_view'),
    path('configuration/planning_update_view/<str:pk>',PlanningUpdateView.as_view(),name="planning_update_view"),
    path("configuration/planning_delete_view/<int:pk>", PlanningDeleteView.as_view(), name="planning_delete_view"),

# salle----------------------------------------------------------------------------------------------
    path('configuration/salle_create_view', salle_create_view, name='salle_create_view'),
    path('configuration/salle_update_view/<str:pk>',SalleUpdateView.as_view(),name="salle_update_view"),
    path("configuration/salle_delete_view/<int:pk>",SalleDeleteView.as_view(), name="salle_delete_view"),
    
# Activites------------------------------------------------------------------------------------------
    path('configuration/activite_create_view', activite_create_view, name='activite_create_view'),
    path('configuration/activite_update_view/<str:pk>',ActiviteUpdateView.as_view(),name="activite_update_view"),
    path("configuration/activite_delete_view/<int:pk>", ActiviteDeleteView.as_view(), name="activite_delete_view"),

# Maladie--------------------------------------------------------------------------------------------
    path('configuration/maladie_create_view', maladie_create_view, name='maladie_create_view'),
    path('configuration/maladie_update_view/<str:pk>',MaladieUpdateView.as_view(),name="maladie_update_view"),
    path("configuration/maladie_delete_view/<int:pk>", MaladieDeleteView.as_view(), name="maladie_delete_view"),

#Portes--------------------------------------------------------------------------------------------------
    path('configuration/porte_create_view', porte_create_view, name='porte_create_view'),
    path('configuration/porte_update_view/<str:pk>',PorteUpdateView.as_view(),name="porte_update_view"),
    path("configuration/porte_delete_view/<int:pk>", PorteDeleteView.as_view(), name="porte_delete_view"),

# Abonnement-------------------------------------------------------------------------------------------------
    path('configuration/type_abonnement_create_view', type_abonnement_create_view, name='type_abonnement_create_view'),
    path('configuration/type_abonnement_update_view/<str:pk>',TypeAbonnementUpdateView.as_view(),name="type_abonnement_update_view"),
    path("configuration/type_abonnement_delete_view/<int:pk>", TypeAbonnementDeleteView.as_view(), name="type_abonnement_delete_view"),

# open close salle----------------------------------------------------------------------------------------------------

    path('open_salle/', open_salle, name='open_salle'),
    path('close_salle/', close_salle, name='close_salle'),
    

   

]





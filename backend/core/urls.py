
from django.urls import path
from .views import (IndexView,PlanningTable,SalleTable ,ActivityTable,MaladieTable,PortesTable,AbonnementTable,
                    PlanningCreateView,PlanningUpdateView)



app_name= 'core'


urlpatterns = [
    path("",IndexView.as_view(),name="index",), 
    # path('configuration/',ConfigurationView.as_view(), name='configuration_name'),
    path('configuration/', PlanningTable.as_view(), name='PlanningTable'),
    path('configuration/SalleTable',SalleTable.as_view(), name='SalleTable'),
    path('configuration/ActivityTable',ActivityTable.as_view(), name='ActivityTable'),
    path('configuration/MaladieTable',MaladieTable.as_view(), name='MaladieTable'),
    path('configuration/PortesTable', PortesTable.as_view(), name='PortesTable'),
    path('configuration/AbonnementTable', AbonnementTable.as_view(), name='AbonnementTable'),

    
    
    
    path('configuration/PlanningCreateView', PlanningCreateView, name='PlanningCreateView'),
    path('configuration/PlanningCreateView/<str:pk>',PlanningUpdateView.as_view(),name="PlanningUpdateView"),

    

   

]





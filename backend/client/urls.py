
from django.urls import path
from .views import (ClientCreateView,ClientView,CoachsView,CoachCreateView,
                    PersonnelsView,PersonnelCreateView,AbonnementClientDetail,
                    ClientUpdateView,ClientDeleteView,CoachUpdateView,CoachDeleteView,
                    PersonnelUpdateView,PersonnelDeleteView)


app_name= 'client'


urlpatterns = [
    path('client/', ClientView.as_view(), name='client_name'),
    path('client/create_client', ClientCreateView, name='client_create'),
    path('client/update/<str:pk>',ClientUpdateView.as_view(),name="client_update"),
    path('client/delete/<str:pk>',ClientDeleteView.as_view(),name="client_delete"),


    path('coach/', CoachsView.as_view(), name='coach_name'),
    path('coach/coach_create',CoachCreateView, name='coach_create'),
    path('coach/update/<str:pk>',CoachUpdateView.as_view(),name='coach_update'),
    path('coach/delete/<str:pk>',CoachDeleteView.as_view(),name="coach_delete"),

    
    path('personnels/', PersonnelsView.as_view(), name='personnels_name'),
    path('personnels/personnels_create',PersonnelCreateView, name='personnel_create'),
    path('personnels/update/<str:pk>',PersonnelUpdateView.as_view(),name='personnel_update'),
    path('personnels/delete/<str:pk>',PersonnelDeleteView.as_view(),name="personnel_delete"),
    
    

    path('client/client_detail/<str:pk>',AbonnementClientDetail.as_view(),name='client_detail')

 
   

]

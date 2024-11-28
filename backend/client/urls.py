
from django.urls import path
from .views import (ClientCreateView,ClientView,CoachsView,CoachCreateView,
                    PersonnelsView,PersonnelCreateView,ClientDetailView,
                    ClientUpdateView,ClientDeleteView,CoachUpdateView,CoachDeleteView,
                    PersonnelUpdateView,PersonnelDeleteView,PaiementClientDetail,
                    VirementsCoachDetail,CoachDetail,PresenceCoachDetail,presence_coach,
                    PersonnelDetail,PresenceClientDetail)


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
    
    


    path('client/client_detail/<str:pk>',ClientDetailView.as_view(),name='client_detail'),
    path('client/PaiementClientDetail/<str:pk>',PaiementClientDetail.as_view(),name='paiement_client_detail'),

    path('client/presence_client_detail/<str:pk>',PresenceClientDetail.as_view(),name='presence_client_detail'),



    path('client/CoachDetail/<str:pk>',CoachDetail.as_view(),name='CoachDetail'),
    path('client/virements_coach_detail/<str:pk>',VirementsCoachDetail.as_view(),name='virements_coach_detail'),
    path('client/PresenceCoachDetail/<str:pk>',PresenceCoachDetail.as_view(),name='PresenceCoachDetail'),
    path('client/presence_coach/<str:pk>',presence_coach,name='presence_coach'),


    path('personnels/PersonnelDetail/<str:pk>', PersonnelDetail.as_view(), name='personnel_detail'),


]

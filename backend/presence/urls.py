from django.urls import path, include
from .views import PresencesView,presence_client,PresenceManuelleClient,PresenceManuelleUpdateClient,PresenceManuelleDeleteClient


app_name = 'presence'

urlpatterns = [


    path('presences/', PresencesView.as_view(), name='presences_name'),
    path('presences/presence_client', presence_client, name='presence_client'),
    path('presences/PresenceManuelleClient', PresenceManuelleClient.as_view(), name='PresenceManuelleClient'),
    path('presences/PresenceManuelleUpdateClient/<str:pk>', PresenceManuelleUpdateClient.as_view(), name='PresenceManuelleUpdateClient'),
    path('presences/Presence_manuelle_deleteclient/<str:pk>', PresenceManuelleDeleteClient.as_view(), name='Presence_manuelle_deleteclient'),


]



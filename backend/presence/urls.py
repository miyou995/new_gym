from django.urls import path, include
from .views import PresencesView,presence_client,PresenceManuelleClient,PresenceManuelleUpdateClient,PresenceManuelleDeleteClient, PresenceSSEView


app_name = 'presence'

urlpatterns = [
    path('presences/', PresencesView.as_view(), name='presences_name'),
    path('presences_sse/', PresenceSSEView.as_view(), name='presences_sse'),
    path('presences/presence_client', presence_client, name='presence_client'),
    path('presences/presence_manuelle_client', PresenceManuelleClient.as_view(), name='presence_manuelle_client'),
    path('presences/presence_manuelle_update_client/<str:pk>', PresenceManuelleUpdateClient.as_view(), name='presence_manuelle_update_client'),
    path('presences/Presence_manuelle_delete_client/<str:pk>', PresenceManuelleDeleteClient.as_view(), name='Presence_manuelle_delete_client'),
]



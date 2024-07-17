from django.urls import path, include
from .views import PresencesView,presence_client,PresenceManuelleClient


app_name = 'presence'

urlpatterns = [


    path('presences/', PresencesView.as_view(), name='presences_name'),
    path('presences/presence_client', presence_client, name='presence_client'),
    path('presences/PresenceManuelleClient', PresenceManuelleClient.as_view(), name='PresenceManuelleClient'),


]



from django.urls import path
from .views import  calendar_view,event_data

app_name = 'creneau'


urlpatterns = [
       # path('creneaux/', CreneauxView.as_view(), name='creneaux_name'),
       path('creneaux/', calendar_view, name='creneaux_name'),
       path('creneaux/events/', event_data, name='event_data'),

]   



from django.urls import path, include
from .views import CreneauxView

app_name = 'creneau'


urlpatterns = [
       path('creneaux/', CreneauxView.as_view(), name='creneaux_name'),
]   



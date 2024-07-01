
from django.urls import path
from .views import IndexView,ConfigurationView   



app_name= 'core'


urlpatterns = [
    path("",IndexView.as_view(),name="index",), 
    path('configuration/',ConfigurationView.as_view(), name='configuration_name'),
   
   
   

]

from django.urls import path, include
from .views import PresencesView


app_name = 'presence'

urlpatterns = [












    path('presences/', PresencesView.as_view(), name='presences_name'),



]



from django.urls import path
from .views import  calendar_view,event_data,CreateCreneau,UpdateCreneau,CreneauDeleteView

app_name = 'creneau'


urlpatterns = [
       # path('creneaux/', CreneauxView.as_view(), name='creneaux_name'),
       path('creneaux/', calendar_view, name='creneaux_name'),
       path('creneaux/events/', event_data, name='event_data'),
       path('creneaux/CreateCreneau',CreateCreneau.as_view(), name='create_creneau'),
       path("creneaux/UpdateCreneau/<int:pk>", UpdateCreneau.as_view(), name="update_creneau"),
       path("creneaux/CreneauDeleteView/<int:pk>", CreneauDeleteView.as_view(), name="creneau_delete_view"),


]   



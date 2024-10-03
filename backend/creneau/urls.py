from django.urls import path
from .views import  (CreateCreneau,UpdateCreneau,CreneauDeleteView,CalenderView,
                     AbonnementsParCreneau)

app_name = 'creneau'


urlpatterns = [
       path('creneaux/', CalenderView.as_view(), name='creneaux_name'),

       path('creneaux/CreateCreneau',CreateCreneau.as_view(), name='create_creneau'),
       path("creneaux/UpdateCreneau/<int:pk>", UpdateCreneau.as_view(), name="update_creneau"),
       path("creneaux/CreneauDeleteView/<int:pk>", CreneauDeleteView.as_view(), name="creneau_delete_view"),
       path("creneaux/abonnements_par_creneau/<int:pk>", AbonnementsParCreneau.as_view(), name="abonnements_par_creneau"),




       # path("CalenderView/", CalenderView.as_view(), name="CalenderView"),

       

]   






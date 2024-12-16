from django.urls import path
from .views import  (CreateCreneau,UpdateCreneau,CreneauDeleteView,CalenderView,
                     AbonnementsParCreneau,abc_creneau_view,render_calendar)

app_name = 'creneau'


urlpatterns = [
       path('abc_creneau_view/', abc_creneau_view, name='abc_creneau_view'),
       
       path('creneaux/', CalenderView.as_view(), name='creneaux_name'),

       path('creneaux/create_creneau',CreateCreneau.as_view(), name='create_creneau'),
       path("creneaux/update_creneau/<int:pk>", UpdateCreneau.as_view(), name="update_creneau"),
       path("creneaux/creneau_delete_view/<int:pk>", CreneauDeleteView.as_view(), name="creneau_delete_view"),
       path("creneaux/abonnements_par_creneau/<int:pk>", AbonnementsParCreneau.as_view(), name="abonnements_par_creneau"),

       path('render_calendar/', render_calendar, name='render_calendar'),




       # path("CalenderView/", CalenderView.as_view(), name="CalenderView"),

       

]   






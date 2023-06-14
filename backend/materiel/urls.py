from django.urls import path, include
from .views import MaterielAPIView, MaterielListAPIView, MaterielDetailAPIView, MaterielDestroyAPIView,get_materiel_authorization 


app_name = 'materiel'


urlpatterns = [
    path('', MaterielListAPIView.as_view(),  name="materiel"),
    path('<int:pk>/', MaterielDetailAPIView.as_view(), name="materiel-delete"),
    path('create', MaterielAPIView.as_view(),  name="materiel-create"),
    path('delete/<int:pk>/', MaterielDestroyAPIView.as_view(), name="materiel-delete"),
    path('get_materiel_authorization/', get_materiel_authorization, name="get_materiel_authorization"),

]



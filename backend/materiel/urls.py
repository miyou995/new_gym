from django.urls import path, include
from .views import MaterielAPIView, MaterielListAPIView, MaterielDetailAPIView, MaterielDestroyAPIView


app_name = 'materiel'


urlpatterns = [
    path('', MaterielListAPIView.as_view(),  name="materiel"),
    path('<int:pk>/', MaterielDetailAPIView.as_view(), name="materiel-delete"),
    path('create', MaterielAPIView.as_view(),  name="materiel-create"),
    path('delete/<int:pk>/', MaterielDestroyAPIView.as_view(), name="materiel-delete"),
]



from django.urls import path, include
from .views import SalleSportAPIView, SalleSportListAPIView, SalleSportDetailAPIView, SalleSportDestroyAPIView


app_name = 'salle-sport'


urlpatterns = [
    path('', SalleSportListAPIView.as_view(),  name="materiel"),
    path('<int:pk>/', SalleSportDetailAPIView.as_view(), name="materiel-delete"),
    path('create', SalleSportAPIView.as_view(),  name="materiel-create"),
    path('delete/<int:pk>/', SalleSportDestroyAPIView.as_view(), name="materiel-delete"),
]



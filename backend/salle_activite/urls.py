from django.urls import path, include
from .views import SalleAPIView, SalleListAPIView, SalleDetailAPIView, SalleDestroyAPIView, ActivityAPIView, ActivityListAPIView, ActivityDetailAPIView, ActivityDestroyAPIView, presences_by_salle, default_salle

app_name = 'salle-activite'


urlpatterns = [
    path('', SalleListAPIView.as_view(),  name="salle-activite"),
    path('by-salles/', presences_by_salle, name="salle-presences"),
    path('default_salle/', default_salle, name="default_salle"),

    path('delete/<int:pk>/', SalleDestroyAPIView.as_view(),  name="salle-delete"),
    path('<int:pk>/', SalleDetailAPIView.as_view(), name="salle-activite-detail"),
    path('create', SalleAPIView.as_view(),  name="salle-activite-create"),

    path('activite/', ActivityListAPIView.as_view(),  name="activite"),
    path('activite/<int:pk>/', ActivityDetailAPIView.as_view(), name="activite-detail"),
    path('activite/create', ActivityAPIView.as_view(),  name="activite-create"),
    path('activite/delete/<int:pk>/', ActivityDestroyAPIView.as_view(), name="activite-delete"),
]



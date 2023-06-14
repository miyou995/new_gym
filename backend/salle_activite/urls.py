from django.urls import path, include
from .views import SalleAPIView, SalleListAPIView, SalleDetailAPIView, SalleDestroyAPIView, ActivityAPIView, ActivityListAPIView, ActivityDetailAPIView, ActivityDestroyAPIView, presences_by_salle, default_salle, DoorApiViewSet, stop_listening, get_salle_authorization, get_activite_authorization, StartListening, OpenTheDoor
from rest_framework import routers

app_name = 'salle-activite'

router = routers.DefaultRouter()
router.register(r'door', DoorApiViewSet)


urlpatterns = [
    path('', SalleListAPIView.as_view(),  name="salle-activite"),
    path('by-salles/', presences_by_salle, name="salle-presences"),
    path('default_salle/', default_salle, name="default_salle"),
    path('', include((router.urls, 'salle-activite'))),
    path('delete/<int:pk>/', SalleDestroyAPIView.as_view(),  name="salle-delete"),
    path('<int:pk>/', SalleDetailAPIView.as_view(), name="salle-activite-detail"),
    path('create', SalleAPIView.as_view(),  name="salle-activite-create"),

    path('activite/', ActivityListAPIView.as_view(),  name="activite"),
    path('activite/<int:pk>/', ActivityDetailAPIView.as_view(), name="activite-detail"),
    path('activite/create', ActivityAPIView.as_view(),  name="activite-create"),
    path('activite/delete/<int:pk>/', ActivityDestroyAPIView.as_view(), name="activite-delete"),
    path('start_listening/', StartListening.as_view(), name="start_listening"),
    path('openthedoor/<int:pk>/', OpenTheDoor.as_view(), name="OpenTheDoor"),
    # path('start_listening/', start_listening, name="start_listening"),
    path('stop_listening/', stop_listening, name="stop_listening"),
    path('get_salle_authorization/', get_salle_authorization, name="get_salle_authorization"),
    path('get_activite_authorization/', get_activite_authorization, name="get_activite_authorization"),
]



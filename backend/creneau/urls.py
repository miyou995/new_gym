from django.urls import path, include
from .views import CreneauAPIView, CreneauPerSalleListAPIView, CreneauListAPIView, CreneauDetailAPIView, CreneauDestroyAPIView, CreneauActivityListAPIView, CreneauByAbonnement, CreneauClientListAPIView, CreneauCoachListAPIView, CreneauBySalleAndPlanningListAPIView, CreneauAbcListAPIView, CreneauByAbndPlanListAPIView


app_name = 'creneau'


urlpatterns = [
    path('by-salle-planning', CreneauBySalleAndPlanningListAPIView.as_view(), name="creneau-salle-planning"),
    path('by-salle', CreneauPerSalleListAPIView.as_view(), name="creneau-salle"),
    path('by-ab-plan', CreneauByAbndPlanListAPIView.as_view(), name="creneau-salle"),
    path('by-client', CreneauClientListAPIView.as_view(), name="creneau-client"),
    path('by-coach', CreneauCoachListAPIView.as_view(), name="creneau-coach"),
    path('by-abonnement', CreneauByAbonnement.as_view(), name="creneau-abn"),
    path('by-abc', CreneauAbcListAPIView.as_view(), name="creneau-abc"),
    path('all/', CreneauListAPIView.as_view(), name="creneau"),
    path('create/', CreneauAPIView.as_view(),  name="creneau-create"),
    path('<int:pk>/', CreneauDetailAPIView.as_view(),  name="creneau-detail"),
    path('delete/<int:pk>/', CreneauDestroyAPIView.as_view(), name="creneau-delete"),
    path('range/<int:pk>/', CreneauDestroyAPIView.as_view(), name="creneau-delete"),
]   



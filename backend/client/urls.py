from django.urls import path, include
from .views import ClientAPIView, ClientListAPIView, ClientDestroyAPIView, ClientDetailAPIView, PersonnelCreateAPIView, PersonnelListAPIView, PersonnelDetailAPIView, PersonnelDestroyAPIView ,CoachCreateAPIView ,CoachListAPIView ,CoachDetailAPIView ,CoachDestroyAPIView, MaladieCreateAPIView, MaladieViewSet, ClientNameViewAPI,  total_dettes, total_abonnes, ClientPresenceViewAPI, ClientNamesDropListAPIView, MaladieDetailViewAPI, GETClientDetailAPIView
from django.views.generic import TemplateView

app_name = 'client'


urlpatterns = [
    # Clients paths
    # path('', TemplateView.as_view(template_name="index.html")),
    path('clients/', ClientListAPIView.as_view(),  name="client"),
    # path('clients-transactions/', ClientPaeiementsViewAPI.as_view(),  name="client-transactions"),
    path('clients-dettes/', total_dettes,  name="client-dettes"),
    path('clients-count/', total_abonnes,  name="client-nombre"),
    path('clients-name/', ClientNameViewAPI.as_view(),  name="client-name"),
    path('clients-name-drop/', ClientNamesDropListAPIView.as_view(),  name="client-name"),
    path('clients-presence/', ClientPresenceViewAPI.as_view(),  name="client-presence"),
    path('clients/<str:pk>/', ClientDetailAPIView.as_view(), name="client-detail"),
    path('get-client/', GETClientDetailAPIView.as_view(), name="client-detail"),

    path('clients/create', ClientAPIView.as_view(),  name="client-create"),
    path('clients/delete/<str:pk>/', ClientDestroyAPIView.as_view(), name="client-delete"),
    # Personnel paths
    path('personnel/', PersonnelListAPIView.as_view(),  name="personnel"),
    path('personnel/<int:pk>/', PersonnelDetailAPIView.as_view(), name="personnel-detail"),
    path('personnel/create', PersonnelCreateAPIView.as_view(),  name="personnel-create"),
    path('personnel/delete/<int:pk>/', PersonnelDestroyAPIView.as_view(), name="personnel-delete"),
        # Coach CoachListAPIView
    path('coachs/', CoachListAPIView.as_view(),  name="coach"),
    path('coachs/<int:pk>/', CoachDetailAPIView.as_view(), name="coach-detail"),
    path('coachs/create', CoachCreateAPIView.as_view(),  name="coach-create"),
    path('coachs/delete/<int:pk>/', CoachDestroyAPIView.as_view(), name="coach-delete"),


    path('maladies/', MaladieViewSet.as_view({'get':'list'}), name="maladie-create-list"),
    path('maladie/create/', MaladieCreateAPIView.as_view(), name="maladie-create"),
    path('maladie/<int:pk>', MaladieDetailViewAPI.as_view(), name="maladie-detail"),
]



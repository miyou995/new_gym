from django.urls import path

from .views import (
    ClientArchiveAbonnement,
    ClientArchivPaiement,
    ClientArchivPresence,
    ClientCreateView,
    ClientDeleteView,
    ClientDetailView,
    ClientUpdateView,
    ClientView,
    CoachCreateView,
    CoachDeleteView,
    CoachDetail,
    CoachsView,
    CoachUpdateView,
    PaiementClientDetail,
    PersonnelCreateView,
    PersonnelDeleteView,
    PersonnelDetail,
    PersonnelsView,
    PersonnelUpdateView,
    PresenceClientDetail,
    PresenceCoachDetail,
    VirementsCoachDetail,
    presence_coach,
)

app_name = "client"


urlpatterns = [
    path("client/", ClientView.as_view(), name="client_name"),
    path("client/create_client", ClientCreateView, name="client_create"),
    path("client/update/<str:pk>", ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<str:pk>", ClientDeleteView.as_view(), name="client_delete"),
    path("coach/", CoachsView.as_view(), name="coach_name"),
    path("coach/coach_create", CoachCreateView, name="coach_create"),
    path("coach/update/<str:pk>", CoachUpdateView.as_view(), name="coach_update"),
    path("coach/delete/<str:pk>", CoachDeleteView.as_view(), name="coach_delete"),
    path("personnels/", PersonnelsView.as_view(), name="personnels_name"),
    path("personnels/personnels_create", PersonnelCreateView, name="personnel_create"),
    path(
        "personnels/update/<str:pk>",
        PersonnelUpdateView.as_view(),
        name="personnel_update",
    ),
    path(
        "personnels/delete/<str:pk>",
        PersonnelDeleteView.as_view(),
        name="personnel_delete",
    ),
    path(
        "client/client_detail/<str:pk>",
        ClientDetailView.as_view(),
        name="client_detail",
    ),
    path(
        "client/paiement_client_detail/<str:pk>",
        PaiementClientDetail.as_view(),
        name="paiement_client_detail",
    ),
    path(
        "client/presence_client_detail/<str:pk>",
        PresenceClientDetail.as_view(),
        name="presence_client_detail",
    ),
    path("client/coach_detail/<str:pk>", CoachDetail.as_view(), name="coach_detail"),
    path(
        "client/virements_coach_detail/<str:pk>",
        VirementsCoachDetail.as_view(),
        name="virements_coach_detail",
    ),
    path(
        "client/presence_coach_detail/<str:pk>",
        PresenceCoachDetail.as_view(),
        name="presence_coach_detail",
    ),
    path("client/presence_coach/<str:pk>", presence_coach, name="presence_coach"),
    path(
        "personnels/personnel_detail/<str:pk>",
        PersonnelDetail.as_view(),
        name="personnel_detail",
    ),
    # archive---------------
    path(
        "client/client_archive_abonnement/<str:pk>",
        ClientArchiveAbonnement.as_view(),
        name="client_archive_abonnement",
    ),
    path(
        "client/client_archive_paiement/<str:pk>",
        ClientArchivPaiement.as_view(),
        name="client_archive_paiement",
    ),
    path(
        "client/client_archive_presence/<str:pk>",
        ClientArchivPresence.as_view(),
        name="client_archive_presence",
    ),
]

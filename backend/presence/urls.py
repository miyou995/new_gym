from django.urls import path, include
from .views import PresenceListAPIView, PresenceDetailAPIView, PresenceDestroyAPIView, PresenceEditAPIView,PresenceCoachCreateAPI,PresenceCoachListAPI,PresenceCoachDetailUpdateAPI,PresenceCoachDestroyAPI, PresenceCoachEditAPIView, PresenceClientDetailAPI, PresenceByCoachListAPI, PresenceClientIsInAPI, PresencePostAPIView, PresenceClientAutoCreateAPI, AllPresenceListAPIView, PresenceHistoryListAPIView, PresenceManualEditAPIView, get_presence_authorization, get_presence_coach_authorization, NotifyPresenceListAPIView


app_name = 'presence'

urlpatterns = [

    path('', PresenceListAPIView.as_view()),
    path('all', AllPresenceListAPIView.as_view()),
    path('auto-create', PresenceClientAutoCreateAPI.as_view()),
    path('presence-create', PresencePostAPIView.as_view(),  ),
    path('client/', PresenceClientDetailAPI.as_view(),  ),
    path('history/', PresenceHistoryListAPIView.as_view(),  ),

    path('coachs/', PresenceCoachListAPI.as_view(), ),
    path('by-coachs/', PresenceByCoachListAPI.as_view(), name="presence-by-coach"),
    path('is-in/', PresenceClientIsInAPI.as_view(), name="presence-in-salle"),
    path('coachs/<int:pk>/', PresenceCoachDetailUpdateAPI.as_view(), name="presence-detail"),
    
    # path('detail/<int:pk>/', PresenceDetailAPIView.as_view(), name="presence-detail"),
    
    path('coachs/create', PresenceCoachCreateAPI.as_view(),  name="presence-coach-create"),
    path('coachs/delete/<int:pk>/', PresenceCoachDestroyAPI.as_view(), name="presence-delete"),
    path('coach/edit/<int:pk>/', PresenceCoachEditAPIView.as_view(), name="presence-edit"),

    path('edit/<int:pk>/', PresenceEditAPIView.as_view(), name="presence-edit"),
    path('manual-edit/<int:pk>/', PresenceManualEditAPIView.as_view(), name="presence-manual"),
    path('<int:pk>/', PresenceDetailAPIView.as_view(), name="presence-detail"),
    path('notification_outputs', NotifyPresenceListAPIView.as_view()),
    
    # path('detail/<int:pk>/', PresenceDetailAPIView.as_view(), name="presence-detail"),

    # path('create', PresenceAPIView.as_view(),  name="presence-create"),
    path('delete/<int:pk>/', PresenceDestroyAPIView.as_view(), name="presence-delete"),
    path('get_presence_authorization/', get_presence_authorization, name="get_presence_authorization"),
    path('get_presence_coach_authorization/', get_presence_coach_authorization, name="get_presence_coach_authorization"),

]



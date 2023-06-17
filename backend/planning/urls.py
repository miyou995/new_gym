from django.urls import path, include
from .views import PlanningAPIView, PlanningListAPIView, PlanningDetailAPIView, PlanningDestroyAPIView, default_planning, get_planning_authorization 


app_name = 'planning'


urlpatterns = [
    path('', PlanningListAPIView.as_view(),  name="planning"),
    path('<int:pk>/', PlanningDetailAPIView.as_view(), name="planning-delete"),
    path('default_planning/', default_planning, name="default_planning"),
    path('create', PlanningAPIView.as_view(),  name="planning-create"),
    path('delete/<int:pk>/', PlanningDestroyAPIView.as_view(), name="planning-delete"),
    path('get_planning_authorization/', get_planning_authorization, name="get_planning_authorization"),

]



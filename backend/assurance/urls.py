from django.urls import path, include
from .views import AssuranceAPIView, AssuranceListAPIView, AssuranceDetailAPIView, AssuranceDestroyAPIView


app_name = 'assurance'


urlpatterns = [
    path('', AssuranceListAPIView.as_view(),  name="assurance"),
    path('<int:pk>/', AssuranceDetailAPIView.as_view(), name="assurance-delete"),
    path('create', AssuranceAPIView.as_view(),  name="assurance-create"),
    path('delete/<int:pk>/', AssuranceDestroyAPIView.as_view(), name="assurance-delete"),


]



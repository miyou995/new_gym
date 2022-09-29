from django.urls import path, include
from rest_framework import routers
from .views import ChangePasswordView, UpdateProfileView, UserDetailAPIView, SignUpView, LoginView, DeleteUserView, GetUsersView, BlacklistTokenUpdateView, GetGroupsView
from rest_framework_simplejwt.views import TokenRefreshView





urlpatterns = [

    path('register', SignUpView.as_view()),
    path('change_password', ChangePasswordView.as_view()),
    path('users/', GetUsersView.as_view()),
    path('groups/', GetGroupsView.as_view()),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name="user-detail"),
    path('delete/:id', DeleteUserView.as_view()),
    path('logout/blacklist', BlacklistTokenUpdateView.as_view(),name='blacklist'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
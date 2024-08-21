from django.urls import path
from .views import SignupView, SignupsuccessView
from django.contrib.auth import views as auth_views
from .froms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .views import (UserDetailView, UserUpdateView, UserListView,
                      change_password,CustomLoginView,UserCreateView,logout_view,
                    UserDeleteView,add_edit_group,
                   GroupDetailView,GroupListView,GroupDeleteView )
from django.urls import reverse_lazy
app_name= 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name="signup"),
    path('signup_success/', SignupsuccessView.as_view(), name="signup_success"),
    
    path('login/', CustomLoginView.as_view(
        template_name="accounts/login.html",
        form_class=AuthenticationForm,
     ), name='login'),
    
    path('userdetail/<int:pk>', login_required(UserDetailView.as_view()), name="userdetail"),
    path('edituser/<int:pk>/', login_required(UserUpdateView.as_view()), name="edituser"),
    path('userlist/', login_required(UserListView.as_view()), name="userlist"),
    path('change_password/<int:pk>/', login_required(change_password), name="change_password"),


    path('UserCreateView/', UserCreateView.as_view(), name="user_create_view"),
    path('logout/', logout_view, name='logout'),
    path('UserDeleteView/<int:pk>/', UserDeleteView.as_view(), name='user_delete_view'),

     ###### PASSWORD RESET ##############
    path('password_reset/' , auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name= "registration/password_reset_email.html",
        success_url = reverse_lazy('accounts:password_reset_done'),), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(
                    template_name='registration/password_change_form.html',
                    success_url = reverse_lazy('accounts:password_reset_complete'), 
                ), 
                name='password_reset_confirm'),
    path('password_reset/complete/' , auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),


    ###### ROLES ##############
    path('grouplist/', login_required(GroupListView.as_view()), name="grouplist"),
    path("create_role/", add_edit_group, name="create_role"),
    path("edit_role/<int:pk>/", add_edit_group, name="edit_role"),

    path('role_detail/<int:pk>/', GroupDetailView.as_view(), name="role_detail"),
    path("delete_group/<int:pk>/", GroupDeleteView.as_view(), name="delete_group"),

]   




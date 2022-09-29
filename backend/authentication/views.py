from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, status, permissions
# from django.contrib.auth.models import User
from django.conf import settings
from authentication.models import User
from django.contrib.auth.models import Group 
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework import pagination

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer, ReadUsersView, ObtainTokenSerializer, GroupSerializer
from django.views.decorators.csrf import ensure_csrf_cookie , csrf_protect
from django.utils.decorators import method_decorator
# Create your views here.
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
# @method_decorator(csrf_protect, name='dispatch')
from rest_framework_simplejwt.views import TokenObtainPairView
# @method_decorator(ensure_csrf_cookie, name='dispatch')

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BaseModelPerm(DjangoModelPermissions):
    def get_custom_perms(self, method, view):
        app_name =  view.queryset.model._meta.app_label
        if hasattr(view, 'extra_perms_map'):
            return [perms for perms in view.extra_perms_map.get(method, [])]
        else:
            return []

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, view.queryset.model)
        perms.extend(self.get_custom_perms(request.method, view))
        return ( request.user and request.user.has_perms(perms) )


class SignUpView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["abonnement.add_user"]
    }

    def post(self, request, format=None):
        data = self.request.data
        print(' LE GFROUP', data['group'])
        email= data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        password= data['password']
        re_password = data['re_password']
        try:
            if password == re_password:
                if User.objects.filter(email=email).exists():
                    return Response({ ' error' : 'nom d\'utilisateur existe déja'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name) 
                    user.save()
                    try:
                        group = Group.objects.get(id=data['group']) 
                        user.groups.add(group)
                        print(' Group=====>', group)
                    except:
                        pass
                    return Response({ 'success' : 'utilisateur creer avec succés'})
            else:
                return Response({ 'error' : 'les mots de pass ne sont pas identique'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error" : "vérifier votre connection"}, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)
            # print('refresh_token',refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # print('eeee',e)
            return Response({"error": "déconnection refusé"},status=status.HTTP_400_BAD_REQUEST)



class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ObtainTokenSerializer


class GetUsersView(generics.ListAPIView):
    queryset = User.objects.prefetch_related('groups')
    serializer_class = ReadUsersView
    pagination_class = StandardResultsSetPagination

    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_user"]
    }

class DeleteUserView(generics.RetrieveUpdateAPIView):
    serializer_class = ReadUsersView
    queryset = User.objects.all()
    extra_perms_map = {
        "GET": ["abonnement.view_user"],
        "PUT": ["abonnement.view_user"],
        "PATCH": ["abonnement.view_user"],
    }

    def get_object(self):
        obj = get_object_or_404(User, id= kwargs["pk"])
        obj.delete()
        return obj

        

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UpdateUserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    extra_perms_map = {
        "GET": ["authentication.add_user"],
        "POST": ["authentication.add_user"],
        "PUT": ["authentication.change_user"],
        "PATCH": ["authentication.change_user"],
        "PATCH": ["authentication.delete_user"],
    }

    # def get_object(self):
    #     obj = get_object_or_404(User, id=kwargs["pk"])
    #     # print('theeeeeeee ', obj , obj.id)
    #     return obj
    

class GetGroupsView(generics.ListAPIView):
    queryset = Group.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer

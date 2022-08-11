from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, status, permissions
# from django.contrib.auth.models import User
from django.conf import settings
from authentication.models import User
from django.contrib.auth.models import Group 
from rest_framework.permissions import AllowAny, IsAuthenticated
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

class SignUpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        data = self.request.data
        print(' LE GFROUP', data['group'])
        group = Group.objects.get(name=data['group']) # HNa lazem fiulter bach njoibou liste ou ndiro for loop najoutiw fiha le group bel wahed
        email= data['email']
        password= data['password']
        re_password = data['re_password']
        try:
            if password == re_password:
                if User.objects.filter(email=email).exists():
                    return Response({ ' error' : 'nom d\'utilisateur existe déja'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.create_user(email=email, password=password) 
                    user.groups.add(group)
                    user.save()
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

# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class GetCSRFTOkent(APIView):
#     permission_classes= (AllowAny,)
#     def get(self, request, format=None):
#         return Response({'success': 'CSRF cookie set'})

class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ObtainTokenSerializer


# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class LoginView(APIView):
#     permission_classes =(AllowAny,)
#     def post(self, request, format=None):
#         data = self.request.data
#         username= data['username']
#         password= data['password']
#         user = auth.authenticate(username=username, password=password)

#         if user is not None:
#             auth.login(request, user)
#             return Response({'success' : 'utilisateur connecté', 'username': username})
#         else : 
#             return Response({ 'error' : 'connection echoué'})

# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class LogOutView(APIView):
#     def post(self, request, format=None):
#         try:
#             auth.logout(request)
#             return Response({'success': ' Déconnection réussit'})
#         except:
#             return Response({ ' error' : 'Déconnection echoué'})

class GetUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ReadUsersView

# class DeleteUserView(APIView):
#     def delete(self, request, format=None):
#         user = self.request.user

#         try :
#             user = User.objects.filter(id=user.id).delete()
#             return Response({"success": "utilisateur supprimé avec succés"})
#         except :
#             return Response({"error": "error lors de la supression"})

 
# @method_decorator(ensure_csrf_cookie, name='dispatch')
class DeleteUserView(generics.RetrieveAPIView):
    serializer_class = ReadUsersView
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)
    # def get(self, request, pk, format=None):
    #     print('THE PK', pk)
    #     print('THE request', request)
    #     user = User.objects.get(id = pk)
    #     user.password = 'abbas+amira=love'
    #     user.save()
    #     # user.objects.delete()
    #     return Response({"success" :" user deleted"})
   
    def get_object(self):
        obj = get_object_or_404(User.objects.filter(id=self.kwargs["pk"]))
        # range = User.objects.filter(hour_start) 
        # print('Salle ... ', User.range.get_clients(21))
        # user = User.objects.get(id = pk)
        # obj.save(update_fields=['password'])
        # print('Salle ... ', self.kwargs)
        print('la choooose,', obj.id)
        del obj 
        return obj

# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer
        

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# class LogoutAllView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         tokens = OutstandingToken.objects.filter(user_id=request.user.id)
#         for token in tokens:
#             t, _ = BlacklistedToken.objects.get_or_create(token=token)

#         return Response(status=status.HTTP_205_RESET_CONTENT)


# class UserAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ReadUsersView

class GetGroupsView(generics.ListAPIView):
    queryset = Group.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ReadUsersView

    def get_object(self):
        obj = get_object_or_404(User.objects.filter(id=self.kwargs["pk"]))
        # print('theeeeeeee ', obj , obj.id)
        return obj
    
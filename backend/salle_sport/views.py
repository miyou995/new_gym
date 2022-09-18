from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import SalleSport
from .serializers import SalleSportSerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.decorators import api_view

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



class SalleSportAPIView(generics.CreateAPIView):
    queryset = SalleSport.objects.all()
    serializer_class = SalleSportSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["salle_sport.add_sallesport"]
    }


class SalleSportListAPIView(generics.ListAPIView):
    queryset = SalleSport.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSportSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["salle_sport.view_sallesport"]
    }

class SalleSportDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = SalleSport.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSportSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["salle_sport.view_sallesport"],
        "PUT": ["salle_sport.change_sallesport"],
        "PATCH": ["salle_sport.change_sallesport"],
    }
    def get_object(self):
        obj = get_object_or_404(SalleSport.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class SalleSportDestroyAPIView(generics.DestroyAPIView):
    queryset = SalleSport.objects.all()
    serializer_class = SalleSportSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["salle_sport.delete_sallesport"],
        "DELETE": ["salle_sport.delete_sallesport"],
    } 

@api_view(['GET'])
def get_sallede_sport_authorization(request):
    user = request.user
    if user.has_perm("salle_sport.view_sallesport"):
        return Response(status=200)
    else:
        return Response(status=403)
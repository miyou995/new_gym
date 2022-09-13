from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Materiel
from .serializers import MaterielSerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions

class BaseModelPerm(DjangoModelPermissions):
    def get_custom_perms(self, method, view):
        app_name = view.model._meta.app_label
        if hasattr(view, 'extra_perms_map'):
            return [app_name+"."+perms for perms in view.extra_perms_map.get(method, [])]
        else:
            return []

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, view.queryset.model)
        perms.extend(self.get_custom_perms(request.method, view))
        return ( request.user and request.user.has_perms(perms) )

class MaterielAPIView(generics.CreateAPIView):
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["materiel.add_materiel"]
    }

class MaterielListAPIView(generics.ListAPIView):
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["materiel.view_materiel"]
    }

class MaterielDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["materiel.change_materiel"]
    }
    def get_object(self):
        obj = get_object_or_404(Materiel.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class MaterielDestroyAPIView(generics.DestroyAPIView):
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["materiel.delete_materiel"]
    }
    
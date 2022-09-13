from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Assurance
from .serializers import AssuranceSerialiser
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

class AssuranceAPIView(generics.CreateAPIView):
    queryset = Assurance.objects.all()
    serializer_class = AssuranceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["assurance.add_assurance"]
    }


class AssuranceListAPIView(generics.ListAPIView):
    queryset = Assurance.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AssuranceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["assurance.view_assurance"]
    }

class AssuranceDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Assurance.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AssuranceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["assurance.change_assurance"]
    }
    def get_object(self):
        obj = get_object_or_404(Assurance.objects.filter(id=self.kwargs["pk"]))
        return obj



class AssuranceDestroyAPIView(generics.DestroyAPIView):
    queryset = Assurance.objects.all()
    serializer_class = AssuranceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["assurance.delete_assurance"]
    }

from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions
from .models import Planning
from .serializers import PlanningSerialiser


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


class PlanningAPIView(generics.CreateAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerialiser
    extra_perms_map = {
        "POST": ["planning.add_planning"]
    }
class PlanningListAPIView(generics.ListAPIView):
    queryset = Planning.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PlanningSerialiser
    extra_perms_map = {
        "GET": ["planning.view_planning"]
    }

class PlanningDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Planning.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PlanningSerialiser
    extra_perms_map = {
        "GET": ["planning.change_planning"],
        "PUT": ["planning.change_planning"],
        "PATCH": ["planning.change_planning"],
    }
    def get_object(self):
        obj = get_object_or_404(Planning.objects.filter(id=self.kwargs["pk"]))
        print('theeeeeeee ', obj , obj.id)
        return obj
    
    def put(self, request, *args, **kwargs):
        #  actuel = Planning.objects.get(pk = instance.id) 
        # plan = Planning.objects.update(salle_sport=request['salle_sport']['name'], name=request['name'])
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print("PATCHHHHHHHHH")
        return self.update(request, *args, **kwargs)


class PlanningDestroyAPIView(generics.DestroyAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerialiser
    extra_perms_map = {
        "POST": ["planning.delete_planning"],
        "DELETE": ["planning.delete_planning"],
    }

@api_view(['GET'])
def default_planning(request):
    planning = Planning.custom_manager.default_planning()
    serializer = PlanningSerialiser(planning, many=False)
    return Response( {'default_planning': serializer.data}) 

    
@api_view(['GET'])
def get_planning_authorization(request):
    user = request.user
    if user.has_perm("planning.view_planning"):
        return Response(status=200)
    else:
        return Response(status=403)


from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Salle, Activity, Door
from .serializers import SalleSerialiser, ActivitySerialiser, DoorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet, ModelViewSet
from .tasks import start_linsten_1, start_linsten_2, start_linsten_3, start_linsten_4, start_linsten_5, start_linsten_6, start_linsten_7, start_linsten_8, start_linsten_9, start_face_door_1, start_face_door_2
from celery.app import default_app
from .device import AccessControl
from rest_framework.views import APIView
from celery import group
import logging
logger = logging.getLogger('salle_activite_view')

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

class DoorApiViewSet(ModelViewSet):
    serializer_class = DoorSerializer
    queryset = Door.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["salle_activite.view_door"],
        "POST": ["salle_activite.add_door"],
        "PUT": ["salle_activite.change_door"],
        "PATCH": ["salle_activite.change_door"],
        "DELETE": ["salle_activite.delete_door"],
    }


class SalleAPIView(generics.CreateAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["salle_activite.add_salle"]
    }

class SalleListAPIView(generics.ListAPIView):
    queryset = Salle.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["salle_activite.view_salle"]
    }

class SalleDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Salle.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["salle_activite.view_salle"],
        "PUT": ["salle_activite.change_salle"],
        "PATCH": ["salle_activite.change_salle"],
    }
    def get_object(self):
        obj = get_object_or_404(Salle.objects.filter(id=self.kwargs["pk"]))
        print('Salle ... ', obj , obj.id)
        return obj
    

class SalleDestroyAPIView(generics.DestroyAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["salle_activite.delete_salle"],
        "DELETE": ["salle_activite.delete_salle"]
    }

class ActivityAPIView(generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["salle_activite.add_activity"]
    }
    def post(self, request, format=None):
        print(request.data)
        serializer = ActivitySerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = 'Activité Creer avec succés'
            return Response({'success': msg}, status=status.HTTP_200_OK)
        else:
            msg = 'erreur : Activité non Creer'
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)



class ActivityListAPIView(generics.ListAPIView):
    queryset = Activity.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ActivitySerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["salle_activite.view_activity"]
    }

class ActivityDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Activity.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ActivitySerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["salle_activite.view_activity"],
        "PUT": ["salle_activite.change_activity"],
        "PATCH": ["salle_activite.change_activity"],
    }
    def get_object(self):
        obj = get_object_or_404(Activity.objects.filter(id=self.kwargs["pk"]))
        print('ACTIVITé ', obj , obj.id)
        return obj
    

class ActivityDestroyAPIView(generics.DestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["salle_activite.delete_activity"],
        "DELETE": ["salle_activite.delete_activity"],
    }

@api_view(['GET'])
def presences_by_salle(request):
    salles = Salle.objects.values('name').annotate(Count('actvities__creneaux__presenses'))
    return Response( {'presences': salles})

@api_view(['GET'])
def default_salle(request):
    default_salle = Salle.custom_manager.default_salle()
    serializer = SalleSerialiser(default_salle, many=False)
    print('la samme', serializer.data)
    return Response( {'default_salle': serializer.data})


class StartListening(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        """
        Open All The Doors
        """
        logger.info("View inited...")
        taks_group = group(
            start_linsten_1.delay(),
            start_linsten_2.delay(),
            start_linsten_3.delay(),
            start_linsten_4.delay(),
            # start_linsten_5.delay(),
            # start_linsten_6.delay(),
            # start_linsten_7.delay(),
            # start_linsten_8.delay(),
            # start_linsten_9.delay(),
            # start_face_door_1.delay(),
            # start_face_door_2.delay()
        )
        return Response(status=200)

class StartListeningTwo(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        """
        Open All The Doors
        """
        logger.info("View inited...")
        taks_group = group(
            start_linsten_1.delay(),
            start_linsten_2.delay(),
            start_linsten_3.delay(),
            start_linsten_4.delay(),
            start_linsten_5.delay(),
            start_linsten_6.delay(),
            start_linsten_7.delay(),
            start_linsten_8.delay(),
            start_linsten_9.delay(),
            start_face_door_1.delay(),
            start_face_door_2.delay()
        )
        return Response(status=200)
# @api_view(['GET'])
# def start_listening(request):
#     print(' before delay')
#     start_linsten_1.delay()
#     # start_linsten_2.delay()
#     print(' AFTER delay')
#     return Response(status=403)

    
@api_view(['GET'])
def stop_listening(request):
    default_app.control.revoke[
        start_linsten_1,
        start_linsten_2,
        start_linsten_3,
        start_linsten_4,
        start_linsten_5,
        start_linsten_6,
        start_linsten_7,
        start_linsten_8,
        start_linsten_9,
        start_face_door_1,
        start_face_door_2
    ]
    print(' AFTER delay')
    return Response( "hello")

    
@api_view(['GET'])
def get_salle_authorization(request):
    user = request.user
    if user.has_perm("salle_activite.view_salle"):
        return Response(status=200)
    else:
        return Response(status=403)

    
@api_view(['GET'])
def get_activite_authorization(request):
    user = request.user
    if user.has_perm("salle_activite.view_activite"):
        return Response(status=200)
    else:
        return Response(status=403)


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
from .tasks import start_linsten_1, start_linsten_2
from .device import AccessControl

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

from rest_framework.views import APIView

class StartListening(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        """
        Open All The Doors
        """
        print('IT S WORKING ')
        start_linsten_1.delay()

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
    print(' before delay')
    device = AccessControl()
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    device.login()
    device.logout()

    device_2 = AccessControl()
    device_2.get_login_info(ip='192.168.1.3', port=37777, username='admin', password='123456')
    device_2.login()
    device_2.logout()
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
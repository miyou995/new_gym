import sys
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db.models import Count
# from rest_framework.response import Response 
from django.db.models import Sum
from rest_framework import generics
from rest_framework import pagination
from rest_framework import filters
from rest_framework.settings import perform_import
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Presence, PresenceCoach
from .serializers import PresenceSerialiser,  PresenceEditSerialiser, PresenceCoachSerializer, PresenceClientSerialiser, PresencePostSerialiser, PresenceAutoSerialiser, PresenceHistorySerialiser, PresenceManualEditSerialiser

from datetime import date, timedelta, datetime

class BaseModelPerm(DjangoModelPermissions):
    def get_custom_perms(self, method, view):
        # app_name =  view.queryset.model._meta.app_label
        if hasattr(view, 'extra_perms_map'):
            return [perms for perms in view.extra_perms_map.get(method, [])]
        else:
            return []

    def has_permission(self, request, view, model=None):
        perms = self.get_required_permissions(request.method, view.queryset.model)
        perms.extend(self.get_custom_perms(request.method, view))
        return ( request.user and request.user.has_perms(perms) )



class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# class PresenceAPIView(generics.CreateAPIView):
#     queryset = Presence.objects.all()
#     serializer_class = PresenceCreateSerialiser

class PresencePostAPIView(generics.CreateAPIView):
    queryset = Presence.objects.all()
    serializer_class = PresencePostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["presence.add_presence"]
    }
    # def create(self, request, format =''):
    #     serializer = self.get_serializer(data=request.data)
    #     presence = serializer.instance
    #     print('ppresence validate data', presence)

    #     if serializer.is_valid():

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        # self.perform_create(serializer)
        # print('hello create presnce',type( serializer.instance), serializer.data)
        # headers = self.get_success_headers(serializer.data)
        # presence = serializer.instance
        # print('ppresence validate data', presence)
        # if not presence.hour_sortie:
        #     serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PresenceHistoryListAPIView(generics.ListAPIView):
    queryset = Presence.history.all()
    pagination_class = StandardResultsSetPagination
    # print('queryset', queryset.count())
    # permission_classes = (IsAuthenticated,)
    serializer_class = PresenceHistorySerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"]
    }

class AllPresenceListAPIView(generics.ListAPIView):
    queryset = Presence.objects.all()
    # permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # search_fields = ['=client__id']
    filterset_fields = ['creneau__activity', 'abc__client_id', 'creneau__activity__salle']
    # filter_backends = (filters.SearchFilter,)

    serializer_class = PresenceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"]
    }



     
class PresenceListAPIView(generics.ListAPIView):
    queryset = Presence.objects.select_related('abc', 'abc__client','creneau')
    # permission_classes = (IsAuthenticated,)
    serializer_class = PresenceSerialiser
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"]
    }
    filterset_fields = ['creneau__activity', 'abc__client_id', 'creneau__activity__salle']

    def get_queryset(self):
        FTM = '%H:%M'
        queryset = Presence.objects.select_related('creneau', 'abc', 'abc__client', 'abc__type_abonnement', 'creneau__activity__salle', 'creneau__planning').annotate(
            total_dette=Sum('abc__client__abonnement_client__reste')
        )        
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        hour = self.request.query_params.get('hour', None) 
        if hour:
            i_start_time = datetime.strptime(hour, FTM)
            i_end_time = i_start_time + timedelta(minutes=20)

            start_time = i_start_time.time() 
            end_time = i_end_time.time()
        try:
            print('ONE²')
            queryset = queryset.filter(date__range=[start_date, end_date], creneau__hour_start__range=[start_time, end_time])
            return queryset.order_by('-id')
        except:
            print('deuxeme')
            queryset = queryset.filter(date__range=[start_date, end_date])
            return queryset.order_by('-id')
        
# from django.utils.dateparse import parse_datetime

# class PresenceListAPIView(generics.ListAPIView):
#     serializer_class = PresenceSerialiser
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [DjangoFilterBackend]
#     # permission_classes = (IsAdminUser, BaseModelPerm)
#     permission_classes = (IsAdminUser, )
#     extra_perms_map = {
#         "GET": ["presence.view_presence"]
#     }
#     filterset_fields = ['creneau__activity', 'abc__client_id', 'creneau__activity__salle']

#     def get_queryset(self):
#         FTM = '%H:%M'
#         queryset = Presence.objects.select_related('creneau', 'abc', 'abc__client', 'abc__type_abonnement', 'creneau__activity__salle', 'creneau__planning').annotate(
#             total_dette=Sum('abc__client__abonnement_client__reste')  # Annotate with the total 'reste'
#         )
#         start_date = self.request.query_params.get('start_date', None)
#         end_date = self.request.query_params.get('end_date', None)
#         hour = self.request.query_params.get('hour', None)

#         if start_date:
#             start_date = parse_datetime(start_date)
#         if end_date:
#             end_date = parse_datetime(end_date)
#         print('self.request.query_params', self.request.query_params.dict())
#         if hour:
#             i_start_time = datetime.strptime(hour, FTM)
#             i_end_time = i_start_time + timedelta(minutes=20)
#             start_time = i_start_time.time()
#             end_time = i_end_time.time()
#             queryset = queryset.filter(creneau__hour_start__range=[start_time, end_time])

#         if start_date and end_date:
#             queryset = queryset.filter(date__range=[start_date, end_date])

#         return queryset.order_by('-id')
        

class PresenceDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PresenceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"],
        "PATCH": ["presence.change_presence"],
        "PUT": ["presence.change_presence"],
    }

class PresenceEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"],
        "PATCH": ["presence.change_presence"],
        "PUT": ["presence.change_presence"],
    }
    
    serializer_class = PresenceManualEditSerialiser

    def put(self, request, *args, **kwargs):
        print(
            self.kwargs
        )
        obj = get_object_or_404(Presence, id=self.kwargs["pk"])
        print('Presence ... ', obj , obj.id)
        client = obj.abc.client
        client.init_output()
        return Response(status=200)

    


class PresenceManualEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"],
        "PATCH": ["presence.change_presence"],
        "PUT": ["presence.change_presence"],
        "PUT": ["presence.change_presence"],
    }
    serializer_class = PresencePostSerialiser
    def get_object(self):
        obj = get_object_or_404(Presence, id=self.kwargs["pk"])
        print('Salle ... ', obj , obj.id)
        return obj


class PresenceDestroyAPIView(generics.DestroyAPIView):
    queryset = Presence.objects.all()
    serializer_class = PresenceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["presence.delete_presence"],
        "DELETE": ["presence.delete_presence"],
    }

class PresenceCoachCreateAPI(generics.CreateAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["presence.add_presencecoach"]
    }
class PresenceCoachListAPI(generics.ListAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presencecoach"]
    }
class PresenceByCoachListAPI(generics.ListAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presencecoach"]
    }
    def get_queryset(self):
        
        coach = self.request.query_params.get('cl', None)
        print('cliiiientr', coach)
        presences = PresenceCoach.objects.filter(coach=coach).distinct()
        return presences



class PresenceCoachDetailUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presencecoach"],
        "PUT": ["presence.change_presencecoach"],
        "PATCH": ["presence.change_presencecoach"],
    }
    def get_object(self):
        obj = get_object_or_404(PresenceCoach.objects.filter(id=self.kwargs["pk"]))
        return obj


class PresenceCoachDestroyAPI(generics.DestroyAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["presence.delete_presencecoach"],
        "DELETE": ["presence.delete_presencecoach"],
    }

    
class PresenceCoachEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"],
        "PUT": ["presence.change_presence"],
        "PATCH": ["presence.change_presence"],
    }
    serializer_class = PresenceEditSerialiser
    def get_object(self):
        obj = get_object_or_404(PresenceCoach.objects.filter(id=self.kwargs["pk"]))

        return obj

class PresenceClientDetailAPI(generics.ListAPIView):
    queryset = Presence.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"]
    }
    serializer_class = PresenceClientSerialiser
    def get_queryset(self):
        client = self.request.query_params.get('cl', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        presences = Presence.objects.filter(abc__client_id=client, date__range=[start_date, end_date]).select_related('creneau', 'abc', 'abc__client', 'abc__type_abonnement', 'creneau__activity__salle', 'creneau__planning').annotate(
            total_dette=Sum('abc__client__abonnement_client__reste')
        )        
        # if start_date and end_date:
        return presences
    

class PresenceClientIsInAPI(generics.ListAPIView):
    queryset = Presence.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"]
    }
    serializer_class = PresenceClientSerialiser
    def get_queryset(self):
        # client = self.request.query_params.filter('cl', None)
        # print('client', client)
        presences = Presence.objects.filter(hour_sortie__isnull=True).select_related('creneau', 'abc', 'abc__client', 'abc__type_abonnement', 'creneau__activity__salle', 'creneau__planning')
        return presences



class PresenceClientAutoCreateAPI(generics.CreateAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceAutoSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["presence.add_presencecoach"],
        "POST": ["presence.add_presence"]
    }


    
@api_view(['GET'])
def get_presence_authorization(request):
    user = request.user
    if user.has_perm("presence.view_presence"):
        return Response(status=200)
    else:
        return Response(status=403)

    
@api_view(['GET'])
def get_presence_coach_authorization(request):
    user = request.user
    if user.has_perm("presence.view_presence_coach"):
        return Response(status=200)
    else:
        return Response(status=403)


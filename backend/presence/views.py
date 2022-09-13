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
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Presence, PresenceCoach
from .serializers import PresenceSerialiser,  PresenceEditSerialiser, PresenceCoachSerializer, PresenceClientSerialiser, PresencePostSerialiser, PresenceAutoSerialiser, PresenceHistorySerialiser, PresenceManualEditSerialiser

from datetime import date, timedelta, datetime

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
        "GET": ["presence.add_presence"]
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
        #     presence.is_in_salle = True
        #     serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PresenceHistoryListAPIView(generics.ListAPIView):
    queryset = Presence.history.all()
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
    queryset = Presence.objects.all()
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
        queryset = Presence.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        hour = self.request.query_params.get('hour', None) 
        # salle = self.request.query_params.get('salle', None)
        # activity = self.request.query_params.get('act', None) 
        # print('" lhaKT §§§')
        if hour:
            i_start_time = datetime.strptime(hour, FTM)
            # print('staaaart', i_start_time)
            i_end_time = i_start_time + timedelta(minutes=20)

            start_time = i_start_time.time() 
            end_time = i_end_time.time()
        try:
            print('ONE²')
            queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__hour_start__range=[start_time, end_time])
            return queryset.order_by('-id')
        except:
            print('deuxeme')
            queryset = Presence.objects.filter(date__range=[start_date, end_date])
            return queryset.order_by('-id')
        else:
            print('FINLMENT')
            return queryset.order_by('-id')
                
            # print('end_time', end_time)
        # else : 
        #     start_time = '01:00:01'
        #     end_time ='23:59:00'
        #     print('sayit b kelech')
        #     try:
        #         print('avec du temps')
        #         print('premier start',start_time)
        #         print('premier start',end_time)
        #         print('je suis queryset', self.request)

        #         return Presence.objects.filter(date__range=[start_date, end_date], creneau__hour_start__range=[start_time, end_time])
        #     except:
        #         print('ALLLL')
        #         print('je suis queryset', self.request)
        # else :
        #     return Presence.objects.all()

        # try:    #HADI LI MCHAT MAIS SANS HEURES
        #     # print('sayit b start_time', start_time)
        #     print('sayit b end_time')
        #     # queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__hour_start__range=[start_time, end_time], creneau__activity__salle=salle, creneau__activity=activity)
        #     queryset = Presence.objects.filter(date__range=[start_date, end_date])
        #     return queryset.order_by('-id')

        # except:
        #     try:
        #         queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__activity__salle=salle, creneau__activity=activity)
        #         return queryset.order_by('-id')
        #     except:
        #         try:
        #             # print('sayit sans acti')
        #             if hour:
        #                 if not activity and not salle:
        #                     queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__hour_start__range=[start_time, end_time])
        #                     # print(' queryyy', queryset)
        #                     return queryset.order_by('-id')
        #                 if not activity:
        #                     # print('sans activité')
        #                     queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__hour_start__range=[start_time, end_time], creneau__activity__salle=salle)
        #                     # queryset = Presence.objects.filter(
        #                     #     Q(date__range=[start_date, end_date]) &
        #                     #     Q(creneau__activity__salle=salle) &
        #                     #     Q(creneau__hour_start__range=[start_time, end_time]) 
        #                     #     )
        #                     # print('sayit b start_time', start_time)
        #                     # print('sayit b end_time', end_time)
        #                     return queryset.order_by('-id')
        #                 elif not salle:
        #                     # print('sans SALLE')
        #                     queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__hour_start__range=[start_time, end_time], creneau__activity=activity)
        #                     # print('sayit b start_time', start_time)
        #                     # print('sayit b end_time', end_time)
        #                     return queryset.order_by('-id')
        #             else:
        #                 if not activity:
        #                     # print('sans activité')
        #                     queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__activity__salle=salle)
        #                     # print('sayit b start_time', start_time)
        #                     # print('sayit b end_time', end_time)
        #                     return queryset.order_by('-id')
        #                 elif not salle:
        #                     # print('sans SALLE')
        #                     queryset = Presence.objects.filter(date__range=[start_date, end_date], creneau__activity=activity)
        #                     # print('sayit b start_time', start_time)
        #                     # print('sayit b end_time', end_time)
        #                     return queryset.order_by('-id')
        #         except:
        #             # print('je suis maaaaaaa')
        #             # queryset = Presence.objects.filter(creneau__activity__salle=1) 
        #             # print('je suis queryset', self.request)
        #             return queryset.order_by('-id')



        

class PresenceDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PresenceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.change_presence"]
    }
    # def get_object(self):
    #     obj = get_object_or_404(Presence.objects.filter(id=self.kwargs["pk"]))
    #     creneaux = Presence.presence_manager.get_presence(30)
    #     # abon = abonnement[0].id
    #     print('get_abonnement..................0....', creneaux)
    #     # #### ce passe dans une fonction
    #     # prenseces = abon.presence_quantity 
    #     # print('ceci est labonnement du client ', abon)

    #     # abonnement.update(presence_quantity = prenseces - 1 )
    #     return obj

class PresenceEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.change_presence"]
    }
    serializer_class = PresenceManualEditSerialiser
    def get_object(self):
        obj = get_object_or_404(Presence, id=self.kwargs["pk"])
        print('Salle ... ', obj , obj.id)
        return obj

class PresenceManualEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.change_presence"]
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
        "GET": ["presence.delete_presence"]
    }

class PresenceCoachCreateAPI(generics.CreateAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.add_presencecoach"]
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
        presences = PresenceCoach.objects.filter(coach=coach)
        return presences



class PresenceCoachDetailUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.change_presencecoach"]
    }
    def get_object(self):
        obj = get_object_or_404(PresenceCoach.objects.filter(id=self.kwargs["pk"]))
        return obj


class PresenceCoachDestroyAPI(generics.DestroyAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceCoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.delete_presencecoach"]
    }

    
class PresenceCoachEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Presence.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.change_presence"]
    }
    serializer_class = PresenceEditSerialiser
    def get_object(self):
        obj = get_object_or_404(PresenceCoach.objects.filter(id=self.kwargs["pk"]))

        # obj = get_object_or_404(Presence.objects.filter(id=self.kwargs["pk"]))
        # creneaux = Presence.presence_manager.get_presence(30)
        # # abon = abonnement[0].id
        # print('get_abonnement..................0....', creneaux)
        # #### ce passe dans une fonction
        # prenseces = abon.presence_quantity 
        # print('ceci est labonnement du client ', abon)

        # abonnement.update(presence_quantity = prenseces - 1 )
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
        presences = Presence.objects.filter(abc__client_id=client, date__range=[start_date, end_date])
        # if start_date and end_date:
        print('presences', presences)
        return presences
    

class PresenceClientIsInAPI(generics.ListAPIView):
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.view_presence"]
    }
    serializer_class = PresenceClientSerialiser
    def get_queryset(self):
        # client = self.request.query_params.filter('cl', None)
        # print('client', client)
        presences = Presence.objects.filter(is_in_salle=True)

        return presences



class PresenceClientAutoCreateAPI(generics.CreateAPIView):
    queryset = PresenceCoach.objects.all()
    serializer_class = PresenceAutoSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["presence.add_presencecoach"]
    }
# class PresencesBySalle(generics.ListAPIView):
#     def get_queryset(self):
#         return presences
    

    # presences = Presence.objects.filter(creneau_activity_salle = Count('client'))



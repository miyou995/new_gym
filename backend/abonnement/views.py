from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta, date
from .serializers import AbonnementClientSerialiser, AbonnementSerialiser, AbonnementClientDetailUpdateSerialiser, AbonnementClientDetailSerializer, AbonnementClientTransactionsSerializer, ABCCreneauSerializer, AbonnementClientRenewSerializer, AbonnementClientAllSerializer, AbonnementClientHistorySerializer
from client.models import Client
from .models import Abonnement,  AbonnementClient
from django.db.models import Prefetch

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 15
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

def is_valid_queryparam(param):
    return param != '' and param is not None

def get_filtered_abc_history(request):
    qs = AbonnementClient.history.select_related('type_abonnement', 'client', 'history_user')
    # qs  =  AbonnementClient.history.select_related(Prefetch('abonnements', queryset=qs))
    # qs = qs.prefetch_related('creneaux')
    start_from = request.query_params.get('start', None)
    end_from = request.query_params.get('end', None)
    usr = request.query_params.get('usr', None)
    cl = request.query_params.get('cl', None)
    abc = request.query_params.get('abc', None)
    if is_valid_queryparam(start_from):
        qs = qs.filter(history_date__gte=start_from).select_related('type_abonnement', 'client', 'history_user')
    if is_valid_queryparam(end_from):
        qs = qs.filter(history_date__lte=end_from).select_related('type_abonnement', 'client', 'history_user')
    if is_valid_queryparam(abc):
        qs = qs.filter(id=abc).select_related('type_abonnement', 'client', 'history_user')  
    if is_valid_queryparam(cl):
        try:
            client = Client.objects.get(id=cl) 
        except:
            client =  get_object_or_404(Client, carte=cl)
        # client = Q( Client.objects.get(id=cl) | Client.objects.get(carte=cl) )
        if client:
            qs = qs.filter(client=client).select_related('type_abonnement', 'client', 'history_user')

    if is_valid_queryparam(usr):
        qs = qs.filter(history_user=usr).select_related('type_abonnement', 'client', 'history_user')
    return {'qs': qs}

class AbonnementClientCreateAPIView(generics.CreateAPIView):
    queryset = AbonnementClient.objects.prefetch_related('type_abonnement', 'creneaux')
    serializer_class = AbonnementClientSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["abonnement.add_abonnementclient"]
    }

class AbonnementClientRenewAPIView(generics.CreateAPIView):
    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientRenewSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["abonnement.view_abonnementclient"]
    }
    
class AbonnementClientListAPIView(generics.ListAPIView):
    queryset = AbonnementClient.objects.filter(archiver=False).prefetch_related('type_abonnement', 'creneaux')
    # permission_classes = (IsAuthenticated,)
    serializer_class = AbonnementClientSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_abonnementclient"]
    }

class AbonnementClientDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = AbonnementClient.objects.prefetch_related('creneaux', 'creneaux__activity').select_related('type_abonnement', 'type_abonnement__salles')
    serializer_class = AbonnementClientDetailUpdateSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_abonnementclient"],
        "PUT": ["abonnement.change_abonnementclient"],
        "PATCH": ["abonnement.change_abonnementclient"],
    }

    def get_object(self):
        obj = get_object_or_404(AbonnementClient.objects.filter(id=self.kwargs["pk"]))
        abon = AbonnementClient.objects.get(id = obj.id)
        print('Test de get client =======> ', abon.transactions.all().aggregate )
        return obj
    

class AbonnementClientDestroyAPIView(generics.DestroyAPIView):
    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientAllSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "DELETE": ["abonnement.delete_abonnementclient"]
    }





class AbonnementAPIView(generics.CreateAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["abonnement.add_abonnementclient"]
    }

class AbonnementListAPIView(generics.ListAPIView):
    queryset = Abonnement.objects.filter(actif=True)
    serializer_class = AbonnementSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_abonnementclient"]
    }

class AbonnementDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Abonnement.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AbonnementSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.change_abonnementclient"],
        "PUT": ["abonnement.change_abonnementclient"],
        "PATCH": ["abonnement.change_abonnementclient"],

    }
    def get_object(self):
        obj = get_object_or_404(Abonnement.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class AbonnementDestroyAPIView(generics.DestroyAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "DELETE": ["abonnement.delete_abonnementclient"]
    }


class DeactivateAbcView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientRenewSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.change_abonnementclient"],
        "PUT": ["abonnement.change_abonnementclient"],
        "PATCH": ["abonnement.change_abonnementclient"],
    }

# class DeactivateAbcView(APIView):
#     def get(self, request, pk, format=None):
#         print('-------------------------------------------------------')
#         abc = self.get_object(pk)
#         abc.put_archiver()
#         serializer = AbonnementClientDetailSerializer(abc)
#         return Response(serializer.data)

class RenewABCView(APIView):
    queryset = AbonnementClient.objects.all()

    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.change_abonnementclient"],
        "POST": ["abonnement.change_abonnementclient"],
        "PUT": ["abonnement.change_abonnementclient"],
        "PATCH": ["abonnement.change_abonnementclient"],
    }
    def get_object(self, pk):
        try:
            return AbonnementClient.objects.get(pk=pk)
        except AbonnementClient.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        abc = self.get_object(pk)
        abc.renew_abc()
        serializer = AbonnementClientDetailSerializer(abc)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        abc = self.get_object(pk)
        abc.renew_abc()
        abc.save()
        serializer = AbonnementClientDetailSerializer(abc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def renew_api_view(request, pk):
#     abc  = AbonnementClient.objects.get( id = pk)
#     abon = abc.type_abonnement
#     jours =   abon.length
#     seances = abon.seances_quantity
#     end_date = abc.end_date
#     delta = timedelta(days = jours)
#     new_start_date = abc.start_date
#     print('DELTA , ', delta)
#     if abc.is_valid():
#         new_start_date = end_date
#         abc.start_date = new_start_date
#         abc.save()
#         if abc.is_time_volume():
#             abc.presence_quantity += seances*60
#         else:
#             abc.presence_quantity += seances
#         # try:
#         #     abc.presence_quantity += seances
#         # except:
#         #     abc.presence_quantity = seances

#         abc.end_date = new_start_date + delta
#         try:
#             abc.reste += abon.price
#         except:
#             abc.reste = abon.price
#         abc.save()
#     else:
#         abc.start_date =  date.today()
#         print('abc start date')
#         abc.end_date = new_start_date + delta
#         abc.presence_quantity = seances
#         try:
#             abc.reste += abon.price
#         except:
#             abc.reste += abon.price
#         abc.save()
#     # print('reqeust', jours, ' heeey', seances)
#     return Response({'new date' : abc.end_date, 'seances': abc.presence_quantity})

class AbonnementClientHistoryListAPIView(generics.ListAPIView):
    queryset = AbonnementClient.history.select_related('type_abonnement', 'client', 'history_user')
    # print('queryset', queryset.count())
    # permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    serializer_class = AbonnementClientHistorySerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.can_view_history"]
    }
    def get_queryset(self):
        queryset = get_filtered_abc_history(self.request)['qs']

        print('queryset HISTOYYYYYYYYYYYYYYYYYYYYYYYY', queryset)
        return queryset

class AbonnementClientAllDetailListApi(generics.ListAPIView):
    queryset = AbonnementClient.objects.all()

    serializer_class = AbonnementClientDetailSerializer    
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_abonnementclient"]
    }
    def get_queryset(self):
        client = self.request.query_params.get('cl', None)
        start_from = self.request.query_params.get('start', None)
        end_from = self.request.query_params.get('end', None)
        ab_type = self.request.query_params.get('ab_type', None)
        print('cliiiientr', client)
        today = date.today()
        abonnements = AbonnementClient.objects.filter(client=client, archiver=False, end_date__gte=start_from, end_date__lte=end_from)
        return abonnements

class AbonnementClientActifsDetailListApi(generics.ListAPIView):
    queryset = AbonnementClient.objects.all()
    # pagination_class = StandardResultsSetPagination

    serializer_class = AbonnementClientDetailSerializer 
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_abonnementclient"]
    }   
    def get_queryset(self):
        client = self.request.query_params.get('cl', None)
        print('cliiiientr', client)
        today = date.today()
        abonnements = AbonnementClient.objects.filter(client=client, archiver=False, end_date__gte=today)
        return abonnements

class AbonnementClientTransactionsDetailListApi(generics.ListAPIView):
    # pagination_class = StandardResultsSetPagination

    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientTransactionsSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_abonnementclient"]
    }    
    # search_fields = ['last_name', 'id', 'first_name', 'faux_id']
    # filter_backends = (filters.SearchFilter,)

class ABClientByCreneauListAPIView(generics.ListAPIView):
    # queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    queryset = AbonnementClient.objects.all()

    serializer_class = ABCCreneauSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["abonnement.view_abonnementclient"]
    }
    def get_queryset(self):
        try:
            creneau = self.request.query_params.get('cr', 1)
            clients = AbonnementClient.objects.filter(creneaux=creneau)
            return clients
        except:
            return None

            
    # def get_serializer_context(self):
    #     creneau = self.request.query_params.get('cr')
    #     return {'creneau':creneau}


@api_view(['GET'])
def total_dettes_abonnee(request):
    client_id = request.query_params.get('cl', None)
    total_abonnees = AbonnementClient.objects.filter(client=client_id).aggregate(Sum('reste'))
    return Response( { 'abonnees': total_abonnees})

@api_view(['GET'])
def total_restes_abonnees(request):
    dettes = AbonnementClient.objects.all().aggregate(Sum('reste'))
    print('dettes--------------------------------',dettes)
    return Response( {'totales_dettes': dettes})

def delete_all(request):
    return Abonnement.objects.all().delete()
    ##### FIN TYPE #####

@api_view(['POST'])
def renew_api_view(request, pk):
    abc  = AbonnementClient.objects.get( id = pk)
    abc.renew_abc()
    print('abc renewed')
    return Response({'message' : "l'abonnement a été renouvelé avec Success"})


@api_view(['GET'])
def deactivate_api_view(request, pk):
    ab  = Abonnement.objects.get( id = pk)
    ab.actif = False 
    ab.save()
    return Response({'message' : "l'abonnement a été suprimer avec Success"})


@api_view(['DELETE'])
def deactivate_abc_api_view(request, pk):
    print('-------------------------------------------------------')
    abc  = AbonnementClient.objects.get( id = pk).delete()
    return Response({'message' : "l'abonnement a été suprimer avec Success"})


@api_view(['GET'])
def get_abonnement_authorization(request):
    user = request.user
    if user.has_perm("abonnement.view_abonnement"):
        return Response(status=200)
    else:
        return Response(status=403)
@api_view(['GET'])
def get_abonnementclient_authorization(request):
    user = request.user
    if user.has_perm("abonnement.view_abonnementclient"):
        return Response(status=200)
    else:
        return Response(status=403)
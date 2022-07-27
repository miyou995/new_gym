from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Abonnement,  AbonnementClient
from .serializers import AbonnementClientSerialiser, AbonnementSerialiser, AbonnementClientDetailUpdateSerialiser, AbonnementClientDetailSerializer, AbonnementClientTransactionsSerializer, ABCCreneauSerializer, AbonnementClientRenewSerializer, AbonnementClientAllSerializer, AbonnementClientHistorySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from datetime import timedelta, date
from rest_framework.response import Response
from client.models import Client
from django.db.models import Sum
from rest_framework.views import APIView
from django.db.models import Q

def is_valid_queryparam(param):
    return param != '' and param is not None

def get_filtered_abc_history(request):
    qs = AbonnementClient.history.all()
    start_from = request.query_params.get('start', None)
    end_from = request.query_params.get('end', None)
    usr = request.query_params.get('usr', None)
    cl = request.query_params.get('cl', None)
    abc = request.query_params.get('abc', None)
    if is_valid_queryparam(start_from):
        qs = qs.filter(history_date__gte=start_from).distinct()
    if is_valid_queryparam(end_from):
        qs = qs.filter(history_date__lte=end_from).distinct()
    if is_valid_queryparam(abc):
        qs = qs.filter(id=abc).distinct()  
    if is_valid_queryparam(cl):
        try:
            client = Client.objects.get(id=cl) 
        except:
            client =  get_object_or_404(Client, carte=cl)
        # client = Q( Client.objects.get(id=cl) | Client.objects.get(carte=cl) )
        if client:
            qs = qs.filter(client=client).distinct()

    if is_valid_queryparam(usr):
        qs = qs.filter(history_user=usr).distinct()
    return {'qs': qs}

class AbonnementClientCreateAPIView(generics.CreateAPIView):
    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientSerialiser


class AbonnementClientRenewAPIView(generics.CreateAPIView):
    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientRenewSerializer

class AbonnementClientListAPIView(generics.ListAPIView):
    queryset = AbonnementClient.objects.filter(archiver=False)
    # permission_classes = (IsAuthenticated,)
    serializer_class = AbonnementClientSerialiser


class AbonnementClientDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = AbonnementClient.objects.all()
    # permission_classes = (IsAuthenticated,)

    serializer_class = AbonnementClientDetailUpdateSerialiser

    def get_object(self):
        obj = get_object_or_404(AbonnementClient.objects.filter(id=self.kwargs["pk"]))
        abon = AbonnementClient.objects.get(id = obj.id)
        print('Test de get client =======> ', abon.transactions.all().aggregate )
        return obj
    

class AbonnementClientDestroyAPIView(generics.DestroyAPIView):
    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientAllSerializer


def delete_all(request):
    return Abonnement.objects.all().delete()
    ##### FIN TYPE #####


class AbonnementAPIView(generics.CreateAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerialiser


class AbonnementListAPIView(generics.ListAPIView):
    queryset = Abonnement.objects.filter(actif=True)
    # permission_classes = (IsAuthenticated,)
    serializer_class = AbonnementSerialiser


class AbonnementDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Abonnement.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AbonnementSerialiser

    def get_object(self):
        obj = get_object_or_404(Abonnement.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class AbonnementDestroyAPIView(generics.DestroyAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerialiser

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

class DeactivateAbcView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AbonnementClient.objects.all()
    serializer_class = AbonnementClientRenewSerializer

# class DeactivateAbcView(APIView):
#     def get(self, request, pk, format=None):
#         print('-------------------------------------------------------')
#         abc = self.get_object(pk)
#         abc.put_archiver()
#         serializer = AbonnementClientDetailSerializer(abc)
#         return Response(serializer.data)

class RenewABCView(APIView):
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
        abc.renew()
        abc.save()
        serializer = AbonnementClientDetailSerializer(abc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def renew_api_view(request, pk):
    abc  = AbonnementClient.objects.get( id = pk)
    abc.renew_abc()
    print('abc renewed')
    return Response({'message' : "l'abonnement a été renouvelé avec Success"})



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
    queryset = AbonnementClient.history.all()
    # print('queryset', queryset.count())
    # permission_classes = (IsAuthenticated,)
    serializer_class = AbonnementClientHistorySerializer
    def get_queryset(self):
        queryset = get_filtered_abc_history(self.request)['qs']
        print('queryset', queryset.count())
        print('queryset', queryset)                                                                                     
        return queryset

class AbonnementClientAllDetailListApi(generics.ListAPIView):
    serializer_class = AbonnementClientDetailSerializer    
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
    serializer_class = AbonnementClientDetailSerializer    
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
    # search_fields = ['last_name', 'id', 'first_name', 'faux_id']
    # filter_backends = (filters.SearchFilter,)

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

class ABClientByCreneauListAPIView(generics.ListAPIView):
    # queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ABCCreneauSerializer
    # permission_classes = (AllowAny, )
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
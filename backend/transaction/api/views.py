from django.shortcuts import render, get_object_or_404
from rest_framework import generics, serializers
from models import Paiement, Autre, AssuranceTransaction, Remuneration, RemunerationProf, Transaction
import json
from client.models import  Coach

from .serializers import PaiementSerialiser, AutreSerialiser, AssuranceSerialiser, RemunerationSerialiser, RemunerationProfSerialiser, TransactionSerialiser, RemunerationProfPostSerialiser,PaiementPostSerialiser, AssurancePostSerialiser, RemunerationPostSerialiser, PaiementFiltersSerialiser, PaiementHistorySerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from drf_multiple_model.views import FlatMultipleModelAPIView, ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from rest_framework import pagination, viewsets, filters
from django.db.models import Count
from salle_activite.models import Salle, Activity
from abonnement.models import Abonnement
from backend.abonnement.api.serializers import AbonnementTestSerializer
from django.http import HttpResponse
from django.http import JsonResponse

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100



class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 15

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


class PaiementAPIView(generics.CreateAPIView):
    queryset = Paiement.objects.all()
    serializer_class = PaiementPostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.add_paiement"]
    }

class PaiementListAPIView(generics.ListAPIView):
    queryset = Paiement.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PaiementSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_paiement"]
    }
class PaiementHistoryListAPIView(generics.ListAPIView):
    queryset = Paiement.history.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PaiementHistorySerialiser
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.can_view_history"]
    }
    # def get_queryset(self):
    #     queryset = get_filtered_abc_history(self.request)['qs']
    #     print('queryset', queryset.count())
    #     print('queryset', queryset)                                                                                     
    #     return queryset

class PaiementDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Paiement.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PaiementPostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_paiement"],
        "PUT": ["transaction.change_paiement"],
        "PATCH": ["transaction.change_paiement"],
    }
    def get_object(self): 
        obj = get_object_or_404(Paiement.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class PaiementDestroyAPIView(generics.DestroyAPIView):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.delete_paiement"],
        "DELETE": ["transaction.delete_paiement"],
    }
# fin des paiement 


class AutreAPIView(generics.CreateAPIView):
    queryset = Autre.objects.all()
    serializer_class = AutreSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.add_autre"]
    }

class AutreListAPIView(generics.ListAPIView):
    queryset = Autre.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AutreSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_autre"]
    }

class AutreDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Autre.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AutreSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_autre"],
        "PUT": ["transaction.change_autre"],
        "PATCH": ["transaction.change_autre"],
    }
    def get_object(self):
        obj = get_object_or_404(Autre.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class AutreDestroyAPIView(generics.DestroyAPIView):
    queryset = Autre.objects.all()
    serializer_class = AutreSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.delete_autre"],
        "DELETE": ["transaction.delete_autre"],
    }
# FIN AUTRE#########

class AssuranceAPIView(generics.CreateAPIView):
    queryset = AssuranceTransaction.objects.all()
    serializer_class = AssurancePostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.add_assurancetransaction"]
    }

class AssuranceListAPIView(generics.ListAPIView):
    queryset = AssuranceTransaction.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AssuranceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_assurancetransaction"]
    }

class AssuranceDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = AssuranceTransaction.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AssurancePostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_assurancetransaction"],
        "PUT": ["transaction.change_assurancetransaction"],
        "PATCH": ["transaction.change_assurancetransaction"],
    }

    def get_object(self):
        obj = get_object_or_404(AssuranceTransaction.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class AssuranceDestroyAPIView(generics.DestroyAPIView):
    queryset = AssuranceTransaction.objects.all()
    serializer_class = AssuranceSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.delete_assurancetransaction"],
        "DELETE": ["transaction.delete_assurancetransaction"],
    }
# FIN ASSURANCE#########

class RemunerationAPIView(generics.CreateAPIView):
    queryset = Remuneration.objects.all()
    serializer_class = RemunerationPostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.add_remuneration"]
    }

class RemunerationListAPIView(generics.ListAPIView):
    queryset = Remuneration.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = RemunerationSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_remuneration"]
    }

class RemunerationDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Remuneration.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = RemunerationPostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_remuneration"],
        "PUT": ["transaction.change_remuneration"],
        "PATCH": ["transaction.change_remuneration"],
    }
    def get_object(self):
        obj = get_object_or_404(Remuneration.objects.filter(id=self.kwargs["pk"]))
        return obj
    
class PaiementEmployeListAPIView(generics.ListAPIView):
    queryset = Remuneration.objects.all()
    serializer_class = RemunerationPostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_remuneration"]
    }
    def get_queryset(self):
        employe_id = self.request.query_params.get('em', None)
        transactions = Remuneration.objects.filter(nom__id=employe_id)
        print('cliiiientr transactions', transactions)
        return transactions

class RemunerationDestroyAPIView(generics.DestroyAPIView):
    queryset = Remuneration.objects.all()
    serializer_class = RemunerationSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.delete_remuneration"],
        "DELETE": ["transaction.delete_remuneration"],
    }

# FIN ASSURANCE#########
class RemunerationProfAPIView(generics.CreateAPIView):
    queryset = RemunerationProf.objects.all()
    serializer_class = RemunerationProfPostSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.add_remunerationprof"]
    }


class RemunerationProfListAPIView(generics.ListAPIView):
    queryset = RemunerationProf.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = RemunerationProfSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_remunerationprof"]
    }
class RemunerationProfDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = RemunerationProf.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_remunerationprof"],
        "PUT": ["transaction.change_remunerationprof"],
        "PATCH": ["transaction.change_remunerationprof"],
    }
    serializer_class = RemunerationProfPostSerialiser
    def get_object(self):
        obj = get_object_or_404(RemunerationProf.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class RemunerationProfDestroyAPIView(generics.DestroyAPIView):
    queryset = RemunerationProf.objects.all()
    serializer_class = RemunerationProfSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["transaction.delete_remunerationprof"],
        "PATCH": ["transaction.delete_remunerationprof"],
    }


class TransactionListAPIView(FlatMultipleModelAPIView):
    queryset = Transaction.objects.all()
    sorting_fields = ['-id']
    filter_backends = (filters.SearchFilter,)
    flat = True
    pagination_class = LimitPagination
    search_fields = ('amount',)
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_transactions"]
    }
    def get_querylist(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        querylist = (
            {
                'queryset': Paiement.objects.filter(date_creation__range=[start_date, end_date]).select_related('abonnement_client', 'abonnement_client__type_abonnement', 'abonnement_client__client').order_by('-date_creation'),
                'serializer_class': PaiementSerialiser,
                'label': 'paiement',
            },
            {
                'queryset': Remuneration.objects.filter(date_creation__range=[start_date, end_date]).select_related('nom').order_by('-date_creation'),
                'serializer_class': RemunerationSerialiser,# il ya un problem
                'label': 'remuneration',
            },
            {
                'queryset': Autre.objects.filter(date_creation__range=[start_date, end_date]).order_by('-date_creation'),
                'serializer_class': AutreSerialiser,
                'label': 'autre',
            },
            {
                'queryset': RemunerationProf.objects.filter(date_creation__range=[start_date, end_date]).select_related('coach').order_by('-date_creation'),
                'serializer_class': RemunerationProfSerialiser,
                'label': 'remunerationProf',
            },
            {
                'queryset': AssuranceTransaction.objects.filter(date_creation__range=[start_date, end_date]).select_related('client').order_by('-date_creation'),
                'serializer_class': AssuranceSerialiser,
                'label': 'assurance',
            },
        )
        return querylist


# class TransactionListAPIView(FlatMultipleModelAPIView):
#     sorting_fields = ['-date_creation']
#     querylist = [
#         {
#             'queryset': Paiement.objects.all().order_by('-date_creation'),
#             'serializer_class': PaiementSerialiser,
#             'label': 'paiement',
#         },
#         {
#             'queryset': Remuneration.objects.all().order_by('-date_creation'),
#             'serializer_class': RemunerationSerialiser,# il ya un problem
#             'label': 'remuneration',
#         },
#         {
#             'queryset': Autre.objects.all().order_by('-date_creation'),
#             'serializer_class': AutreSerialiser,
#             'label': 'autre',
#         },
#         {
#             'queryset': RemunerationProf.objects.all().order_by('-date_creation'),
#             'serializer_class': RemunerationProfSerialiser,
#             'label': 'remunerationProf',
#         },
#         {
#             'queryset': AssuranceTransaction.objects.all().order_by('-date_creation'),
#             'serializer_class': AssuranceSerialiser,
#             'label': 'assurance',
#         },
#      ]
    
    # def get_queryset(self):
    #     return Transaction.objects.select_subclasses()

class TransactionDetailAPIView(generics.RetrieveUpdateAPIView):
    # querylist = [
    #     {
    #         'queryset': Paiement.objects.all(),
    #         'serializer_class': PaiementSerialiser,
    #         'label': 'Paiements',
    #     },
    #     {
    #         'queryset': Remuneration.objects.all(),
    #         'serializer_class': RemunerationSerialiser,
    #         'label': 'Remunerations',
    #     },
    #  ]
    queryset = Transaction.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_transaction"],
        "PUT": ["transaction.change_transaction"],
        "PATCH": ["transaction.change_transaction"],
    }
    serializer_class = TransactionSerialiser

    def get_object(self): 
        obj = get_object_or_404(Transaction.objects.filter(id=self.kwargs["pk"]))
        return obj
    
class PaiementCoachListAPIView(generics.ListAPIView):
    queryset = RemunerationProf.objects.all()
    serializer_class = RemunerationProfPostSerialiser
    permission_classes = (IsAdminUser, BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_remunerationprof"]
    }
    def get_queryset(self):
        coach_id = self.request.query_params.get('cl', None)
        coach = get_object_or_404(Coach, id=coach_id)
        print('cliiiientr', coach)
        transactions = RemunerationProf.objects.filter(coach=coach)
        print(' TRansaction coach -------------------------->', transactions)
        return transactions

@api_view(['GET'])
def total_charges(request):
    charges_coachs = RemunerationProf.objects.filter(amount__gte = 0).aggregate(Sum('amount'))
    charges_personnel = Remuneration.objects.filter(amount__gte = 0).aggregate(Sum('amount'))
    charges_autre = Autre.objects.filter(amount__lte = 0).aggregate(Sum('amount'))
    total_list = [charges_coachs['amount__sum']  , charges_personnel['amount__sum'] , charges_autre['amount__sum']]
    totale = 0

    for i in total_list: 
        if i :
            totale+=i
    print('total autrs', totale)
    return Response( {'total_charges': totale})

class MyModelViewSet(generics.ListAPIView):
    # The usual stuff here
    queryset="""
          SELECT  abonnement_abonnement.id, Sum(amount)  from transaction_paiement join transaction_transaction on transaction_paiement.transaction_ptr_id=transaction_transaction.id
 join abonnement_abonnementclient on transaction_paiement.abonnement_client_id=abonnement_abonnementclient.id 
 join abonnement_abonnement on abonnement_abonnementclient.type_abonnement_id=abonnement_abonnement.id
 join  abonnement_abonnement_salles on abonnement_abonnement.id=  abonnement_abonnement_salles.abonnement_id
 where transaction_transaction.date_creation between '2021-03-01' and '2022-07-01' GROUP BY abonnement_abonnement.name
        """
    model = Abonnement
    serializer_class = AbonnementTestSerializer
    # permission_classes = (IsAdminUser,BaseModelPerm)
    # extra_perms_map = {
    #     "GET": ["transaction.view_client"]
    # }
    def list(self, request):
        queryset = self.get_queryset()
        serializer = AbonnementTestSerializer(list(queryset), many=True)
        return Response(serializer.data)


#@api_view(['GET'])
# def presences_by_salle(request):
#     salles = Salle.objects.values('name').annotate(Count('actvities__creneaux__presenses'))
#     return Response( {'presences': salles})



@api_view(['GET'])
def ca_by_salle(request):
    st_date = request.query_params.get('st', None)
    nd_date = request.query_params.get('nd', None)
    if st_date and nd_date :
        ca = Salle.objects.filter(abonnements__type_abonnement_client__transactions__date_creation__range=[st_date, nd_date]).values('name').annotate(Sum('abonnements__type_abonnement_client__transactions__amount')).order_by('-abonnements__type_abonnement_client__transactions__amount__sum')
    return Response(ca)

@api_view(['GET'])
def ca_by_ab(request):
    st_date = request.query_params.get('st', None)
    nd_date = request.query_params.get('nd', None)
#     query="""
#           SELECT  abonnement_abonnement.id, Sum(amount)  from transaction_paiement join transaction_transaction on transaction_paiement.transaction_ptr_id=transaction_transaction.id
#  join abonnement_abonnementclient on transaction_paiement.abonnement_client_id=abonnement_abonnementclient.id 
#  join abonnement_abonnement on abonnement_abonnementclient.type_abonnement_id=abonnement_abonnement.id
#  join  abonnement_abonnement_salles on abonnement_abonnement.id=  abonnement_abonnement_salles.abonnement_id
#  where transaction_transaction.date_creation between '2021-03-01' and '2022-07-01' GROUP BY abonnement_abonnement.name
#         """
    # ab = Abonnement.objects.raw(query)
    # for i in ab:
    #     print('this is ab..............',type(i))
    
    ab = Abonnement.objects.filter(type_abonnement_client__transactions__date_creation__range=[st_date, nd_date]).values('name').annotate(Sum('type_abonnement_client__transactions__amount'))
    # ab.aggregate(Sum('amount'))
    # ab = Abonnement.objects.values('name').annotate(Sum('type_abonnement_client__transactions__amount')).filter(type_abonnement_client__transactions__date_creation__range=['2021-03-01', '2022-07-01']).order_by('-type_abonnement_client__transactions__amount__sum')
    # hey = serializers.PaiementSerialiser(ab)
    # print('this is ab..............',ab[0])
    return Response( ab)

# @api_view(['GET'])
# def ca_by_activity(request):
#     st_date = request.query_params.get('st', None)
#     nd_date = request.query_params.get('nd', None)
#     if st_date and nd_date :
#         ab = Activity.objects.values('name').annotate(Sum('salle__abonnements__type_abonnement_client__transactions__amount')).order_by('-salle__abonnements__type_abonnement_client__transactions__amount__sum')
#     return Response(ab)

@api_view(['GET'])
def ca_by_date(request):
    st_date = request.query_params.get('st', None)
    nd_date = request.query_params.get('nd', None)
    if st_date and nd_date:
        ttc_autre = Autre.objects.filter(amount__gte = 0).aggregate(Sum('amount'))
        ttc_paiement = Paiement.objects.filter(date_creation__range=[st_date, nd_date]).aggregate(Sum('amount'))
        ttc_assurance = AssuranceTransaction.objects.filter(date_creation__range=[st_date, nd_date]).aggregate(Sum('amount'))
        if not ttc_autre :
            ttc_autre = 0
        if not ttc_paiement :
            ttc_paiement = 0
        if not ttc_assurance :
            ttc_assurance = 0
        total = ttc_paiement['amount__sum'] 
        print('LE TOTAAAAL', total)
        return Response( {'chiffre_affaire': total})

@api_view(['GET'])
def chiffre_affaire(request):

    ttc_autre = Autre.objects.filter(amount__gte = 0).aggregate(Sum('amount'))
    ttc_paiement = Paiement.objects.all().aggregate(Sum('amount'))
    ttc_assurance = AssuranceTransaction.objects.all().aggregate(Sum('amount'))

    if not ttc_autre :
        ttc_autre = 0
    if not ttc_paiement :
        ttc_paiement = 0
    if not ttc_assurance :
        ttc_assurance = 0
    total = ttc_paiement['amount__sum'] 
    print('ELSEEEEE TOTAAAAL', total)

    return Response( {'chiffre_affaire': total})

# @api_view(['GET'])
# def trans_today(request):
#     today = date.today()
#     trans = Transaction.objects.filter(date_creation = today)

#     return Response(trans).data

class TransToday(FlatMultipleModelAPIView):
    queryset = Transaction.objects.all()
    today = date.today()
    sorting_fields = ['-date_creation']
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_transaction"]
    }
    querylist = [
        {
            'queryset': Paiement.objects.filter(date_creation = today).order_by('-date_creation'),
            'serializer_class': PaiementSerialiser,
            'label': 'paiement',
        },
        {
            'queryset': Remuneration.objects.filter(date_creation = today).select_related('nom').order_by('-date_creation'),
            'serializer_class': RemunerationSerialiser,
            'label': 'remuneration',
        },
        {
            'queryset': Autre.objects.filter(date_creation = today).order_by('-date_creation'),
            'serializer_class': AutreSerialiser,
            'label': 'autre',
        },
        {
            'queryset': RemunerationProf.objects.filter(date_creation = today).select_related('coach').order_by('-date_creation'),
            'serializer_class': RemunerationProfSerialiser,
            'label': 'remunerationProf',
        },
        {
            'queryset': AssuranceTransaction.objects.filter(date_creation = today).order_by('-date_creation'),
            'serializer_class': AssuranceSerialiser,
            'label': 'assurance',
        },
     ]
    # def get_queryset(self):
    #     today = date.today()

    #     return Transaction.objects.filter(date_creation = today)

class PaiementClientListAPIView(generics.ListAPIView):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["transaction.view_paiement"]
    }
    def get_queryset(self):
        client = self.request.query_params.get('cl', None)
        transactions = Paiement.objects.filter(abonnement_client__client=client).select_related('abonnement_client__client','abonnement_client', 'abonnement_client__type_abonnement')
        return  transactions



@api_view(['GET'])
def get_transaction_authorization(request):
    user = request.user
    if user.has_perm("transaction.view_transaction"):
        return Response(status=200)
    else:
        return Response(status=403)
    


















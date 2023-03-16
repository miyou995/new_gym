from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from .models import Client, Personnel, Coach, Maladie
from .serializers import ClientSerialiser, PersonnelSerializer, CoachSerializer, MaladieSerializer, ClientNameSerializer, ClientCreateSerialiser, ClientNameDropSerializer, ClientLastPresenceSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from rest_framework import pagination
from rest_framework import filters
from rest_framework import status

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
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
        print('IM has_permission', perms)

        return ( request.user and request.user.has_perms(perms) )


class ClientAPIView(generics.CreateAPIView):
    serializer_class = ClientCreateSerialiser
    queryset = Client.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["client.add_client"]
    }
    # def perform_create(self, serializer):
    #     queryset = SignupRequest.objects.filter(user=self.request.user)
    #     if queryset.exists():
    #         raise ValidationError('You have already signed up')
    #     serializer.save(user=self.request.user)
    # lookup_field = 'slug'
   # permission_classes = (AllowAny, )

class ClientListAPIView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Client.objects.prefetch_related('abonnement_client', 'abonnement_client__creneaux', 'maladies', 'abonnement_client__type_abonnement','abonnement_client__presences')
    # permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerialiser
    # lookup_field = 'slug'
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_client"]
    }
    search_fields = ['=id','last_name',  'first_name', 'phone']


class ClientNamesDropListAPIView(generics.ListAPIView):
    queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ClientNameDropSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_client"]
    }



class GETClientDetailAPIView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ClientLastPresenceSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_client"],
        "PUT": ["client.change_client"],
        "PATCH": ["client.change_client"],
    }

    def get_object(self):
        try:
            client = Client.objects.get(id = self.request.query_params.get('cl', None))
        except :
            client = get_object_or_404(Client, carte=self.request.query_params.get('cl', None))
            # client = Client.objects.get(carte = self.request.query_params.get('cl', None))
        print('object, client', client)
        return client

    # def get(self , request, *args, **kwargs):
    #     params = self.request.query_params.get('cl', None)
    #     print('object,params', params)
    #     try:
    #         client = Client.objects.get(id = params)
    #     except :
    #         client = Client.objects.filter(carte = params)
    #     print('les client !!!', client)
    #     # obj = get_object_or_404(Client.objects.filter(id=self.kwargs["pk"]))
    #     ax = self.serializer_class(client)
    #     return Response(ax.data)

class ClientDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_client"],
        "PUT": ["client.change_client"],
        "PATCH": ["client.change_client"],
    }

    def get_object(self):
        obj = get_object_or_404(Client, id=self.kwargs["pk"])
        return obj
    
    def get(self , request, *args, **kwargs):
        # try:
        obj = get_object_or_404(Client, id=self.kwargs["pk"])

        # obj.is_on_salle()
        ax = self.serializer_class(obj)
        return Response(ax.data)
        # except:
        #     msg = 'le client nexiste pas'
            # return Response({'message': msg}, status=404)


class ClientDestroyAPIView(generics.DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerialiser
    # lookup_field = 'slug'
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["client.delete_client"],
        "DELETE": ["client.delete_client"],
    }
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
################################################
#################  PERSONNEL  ##################
################################################


class PersonnelCreateAPIView(generics.CreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["client.add_personnel"]
    }



class PersonnelListAPIView(generics.ListAPIView):
    queryset = Personnel.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PersonnelSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_personnel"]
    }


class PersonnelDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Personnel.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PersonnelSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_personnel"],
        "PUT": ["client.change_personnel"],
        "PATCH": ["client.change_personnel"],
    }

    def get_object(self):
        obj = get_object_or_404(Personnel, id=self.kwargs["pk"])
        return obj
    

class PersonnelDestroyAPIView(generics.DestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["client.delete_personnel"],
        "DELETE": ["client.delete_personnel"]
    }

###############################################
#################   COACHS   ##################
###############################################
class CoachCreateAPIView(generics.CreateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["client.add_coach"]
    }



class CoachListAPIView(generics.ListAPIView):
    queryset = Coach.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CoachSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_coach"]
    }

class CoachDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Coach.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = CoachSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET":  ["client.view_client"],
        "PUT":  ["client.change_client"],
        "PATCH":["client.change_client"],
    }

    def get_object(self):
        obj = get_object_or_404(Coach.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class CoachDestroyAPIView(generics.DestroyAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["client.delete_coach"],
        "DELETE": ["client.delete_coach"]
    }


class MaladieCreateAPIView(generics.CreateAPIView):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["client.add_maladie"]
    }


class MaladieViewSet(viewsets.ViewSet):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_maladie"],
        "POST": ["client.add_maladie"],
        "PUT": ["client.change_maladie"],
        "PATCH": ["client.change_maladie"],
        "DELETE": ["client.delete_maladie"],
    }

    def list(self, request):
        queryset = Maladie.objects.all()
        serializer = MaladieSerializer(queryset, many=True)
        return Response(serializer.data)


class ClientNameViewAPI(generics.ListAPIView):
    queryset = Client.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_client"]
    }
    serializer_class = ClientNameSerializer
    search_fields = [ '=id','=carte', '^last_name', '^first_name', '^phone']
    filter_backends = (filters.SearchFilter,)

class MaladieDetailViewAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_maladie"],
        "PUT": ["client.change_maladie"],
        "PATCH": ["client.change_maladie"],
        "DELETE": ["client.delete_maladie"],
    }
# class ClientPaeiementsViewAPI(generics.ListAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientTransactionsSerializer

class ClientPresenceViewAPI(generics.ListAPIView):
    # pagination_class = StandardResultsSetPagination
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientNameDropSerializer
    search_fields = ['^last_name', '=id', '^first_name']
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["client.view_client"]
}

@api_view(['GET'])
def total_dettes(request):
    dettes = Client.objects.all().aggregate(Sum('dette'))
    print('les CLIENTS--------------------', Client.objects.first().dette)
    return Response(dettes)

@api_view(['GET'])
def total_abonnes(request):
    total_abonnees = Client.objects.all().count()
    return Response( {'abonnees': total_abonnees})


# @api_view(['GET'])
# def abonnements(request):
#     total_abonnees = Client.objects.all().count()
#     return Response( { 'abonnees': total_abonnees})
#sdvdsvsddsv

@api_view(['GET'])
def get_client_authorization(request):
    user = request.user
    if user.has_perm("client.view_client"):
        return Response(status=200)
    else:
        return Response(status=403)

@api_view(['GET'])
def get_coach_authorization(request):
    user = request.user
    if user.has_perm("client.view_coach"):
        return Response(status=200)
    else:
        return Response(status=403)

@api_view(['GET'])
def get_personnel_authorization(request):
    user = request.user
    if user.has_perm("client.view_personnel"):
        return Response(status=200)
    else:
        return Response(status=403)




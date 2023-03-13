from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Creneau
from salle_activite.models import Salle
from planning.models import Planning
from .serializers import CreneauSerialiser, CreneauxSimpleSerialiser, CreneauClientSerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from abonnement.models import AbonnementClient

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


class CreneauAPIView(generics.CreateAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["creneau.add_creneau"]
    }

class CreneauListAPIView(generics.ListAPIView):
    serializer_class = CreneauSerialiser
    # permission_classes = (IsAuthenticated,)
    queryset = Creneau.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }
class CreneauActivityListAPIView(generics.ListAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }
    def get_queryset(self):
        par = self.request.query_params.get('day', None)
        activ = self.request.query_params.get('act', None)
        return Creneau.objects.filter(day=par, activity=activ)


class CreneauPerSalleListAPIView(generics.ListAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }
    def get_queryset(self):
        salle = self.request.query_params.get('salle', None)
        return Creneau.objects.filter(activity__salle=salle)

class CreneauBySalleAndPlanningListAPIView(generics.ListAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }

    def get_queryset(self):
        salle = self.request.query_params.get('sa', None)
        planning = self.request.query_params.get('pl', None)
        try:
            creneaux = Creneau.objects.filter(activity__salle=salle, planning=planning)
        except:
            creneaux = Creneau.objects.none()
        return creneaux

    # def get_queryset(self):
    #     jour = self.kwargs['day']
    #     # activ = self.kwargs['activity']
    #     creneaux= Creneau.objects.filter(day=jour)
    #     return creneaux
        
class CreneauByAbndPlanListAPIView(generics.ListAPIView):    
    queryset = Creneau.objects.all()
    serializer_class = CreneauSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }

    def get_queryset(self):
        planning = self.request.query_params.get('pl', None)
        type_ab = self.request.query_params.get('ab', None)
        # salle = Salle.objects.get(activities__activities_id= type_ab)
        return Creneau.objects.filter(activity__salle__abonnements__id = type_ab, planning=planning)



class CreneauDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Creneau.objects.all()
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"],
        "PUT": ["creneau.change_creneau"],
        "PATCH": ["creneau.change_creneau"],
    }

    serializer_class = CreneauSerialiser
    def get_object(self):
        obj = get_object_or_404(Creneau.objects.filter(id=self.kwargs["pk"]))
        # range = Creneau.objects.filter(hour_start) 
        # print('Salle ... ', Creneau.range.get_clients(21))
        chose = Creneau.range.get_creneaux_of_day()
        print('la choooose,', chose)
        # print('Salle ... ', self.kwargs)
        return obj

class CreneauDestroyAPIView(generics.DestroyAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "POST": ["creneau.delete_creneau"],
        "DELETE": ["creneau.delete_creneau"],
    }

    
class CreneauByAbonnement(generics.ListAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauxSimpleSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.delete_creneau"]
    }
    def get_queryset(self):
        abonnement_id = self.request.query_params.get('ab', None)
        abc_id = self.request.query_params.get('abc', None)
        abonnement_client = AbonnementClient.objects.get(id=abc_id)
        # planning = Planning.objects.get()
        try:
            planning_id = abonnement_client.creneaux.first().planning.id
            print('PLANNNING ID', planning_id)
            creneaux = Creneau.objects.filter(activity__salle__abonnements__id = abonnement_id,  planning__id=planning_id)
        except:
            creneaux = Creneau.objects.filter(activity__salle__abonnements__id = abonnement_id)
        # print('les ceneaux', creneaux.count())
        return creneaux



class CreneauClientListAPIView(generics.ListAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauClientSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }

    def get_queryset(self):
        client = self.request.query_params.get('cl', None)
        print('cliiiientr', client)
        abc = AbonnementClient.objects.filter(client= client)
        # abc = AbonnementClient.objects.filter(client= client, type_abonnement__systeme_cochage=False)
        # creneaux = Creneau.objects.filter(abonnements__client=client, abonnements__type_abonnement__systeme_cochage=False)
        creneaux = Creneau.objects.filter(abonnements__client=client).distinct()
        return creneaux

class CreneauCoachListAPIView(generics.ListAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauClientSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }

    def get_queryset(self):
        coach = self.request.query_params.get('cl', None)
        print('cliiiientr', coach)
        creneaux = Creneau.objects.filter(coach=coach).distinct()
        return creneaux

class CreneauAbcListAPIView(generics.ListAPIView):
    queryset = Creneau.objects.all()
    serializer_class = CreneauClientSerialiser
    permission_classes = (IsAdminUser,BaseModelPerm)
    extra_perms_map = {
        "GET": ["creneau.view_creneau"]
    }

    def get_queryset(self):
        abonnement = self.request.query_params.get('ab', None)
        creneaux = Creneau.objects.filter(abonnements__id =abonnement)
        return creneaux


@api_view(['GET'])
def get_creneau_authorization(request):
    user = request.user
    if user.has_perm("creneau.view_creneau"):
        return Response(status=200)
    else:
        return Response(status=403)

# @api_view(['GET'])
# def creneau_by_abonnee(request):
#     creneaux = Creneau.objects.filter()
#     return Response({'creneaux': creneaux})



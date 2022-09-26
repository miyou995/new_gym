from .models import Creneau
from rest_framework import serializers
from datetime import timedelta, datetime
from salle_activite.serializers import SalleSerialiser
from salle_activite.models import Salle
from presence.serializers import PresenceSerialiser
# from client.serializers import ClientSerialiser
from client.models import Client
from rest_framework.response import Response

class ClientCreneauxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'last_name')

class CreneauxSimpleSerialiser(serializers.ModelSerializer):
    width       = serializers.SerializerMethodField('get_width', read_only=True)
    coach_name  = serializers.SerializerMethodField('get_coach_name', read_only=True)
    creneau_color       = serializers.SerializerMethodField('get_color', read_only=True)
    salle       = serializers.SerializerMethodField('get_salle', read_only=True)
    activity_name = serializers.CharField(source='activity.name')
    # client_count       = serializers.SerializerMethodField('get_client_count', read_only=True)
    class Meta:
        model = Creneau
        fields= ('id', 'hour_start', 'hour_finish', 'day', 'planning', 'activity', 'activity_name', 'color' , 'creneau_color', 'coach', 'width','coach_name', 'salle' )
        
    def get_color(self, obj):
        # print('la couleur ===>', obj.activity)
        return obj.get_color()
    
    # def get_color(self, obj):
    #     # print('la couleur ===>', obj.activity)
    #     return obj.activity.color
           
    def get_width(self, obj):
        hour1 = str(obj.hour_start)
        hour2 = str(obj.hour_finish)
        FTM = '%H:%M:%S'
        duree_hour =  datetime.strptime(hour2, FTM) - datetime.strptime(hour1, FTM)
        duree_seconde = timedelta.total_seconds(duree_hour) 
        duree_minute = duree_seconde / 60
        # print('hello', duree_minute)
        return duree_minute * 3
    def get_coach_name(self, obj):
        try:
            coach = obj.coach.first_name
        except:
            coach = False
        return coach

    def get_salle(self, obj):
        # print('la salle de ce creneaux est:', obj.activity.salle)
        salle = obj.activity.salle
        acti = salle.name
        # print('th eacti ', acti)
        # queryset = acti.salle.name
        # return SalleSerialiser(queryset, many=False).data
        return acti


class CreneauSerialiser(serializers.ModelSerializer):
    # color       = serializers.CharField(source='coach.color',read_only=True)
    width       = serializers.SerializerMethodField('get_width', read_only=True)
    creneau_color       = serializers.SerializerMethodField('get_color', read_only=True)
    coach_name  = serializers.SerializerMethodField('get_coach_name', read_only=True)
    salle       = serializers.SerializerMethodField('get_salle', read_only=True)
    # presences   = serializers.SerializerMethodField('get_presences', read_only= True)
    # clients   = serializers.SerializerMethodField('get_clients', read_only= True)
    clients_count   = serializers.SerializerMethodField('get_clients_count', read_only= True)
    activity_name   = serializers.SerializerMethodField('get_activity_name', read_only= True)
    class Meta:
        model = Creneau
        fields= ('id', 'name','hour_start', 'hour_finish', 'day', 'planning', 'activity', 'color', 'creneau_color', 'coach', 'width','coach_name', 'salle', 'clients_count', 'activity_name')
        
    def get_color(self, obj):
        # print('la couleur ===>', obj.activity)
        return obj.get_color()
        
    def get_width(self, obj):
        hour1 = str(obj.hour_start)
        hour2 = str(obj.hour_finish)
        FTM = '%H:%M:%S'
        duree_hour =  datetime.strptime(hour2, FTM) - datetime.strptime(hour1, FTM)
        duree_seconde = timedelta.total_seconds(duree_hour) 
        duree_minute = duree_seconde / 60
        # print('hello', duree_minute)
        return duree_minute * 3
    def get_coach_name(self, obj):
        try:
            coach =obj.coach.first_name
        except:
            coach =False
        return coach

    def get_salle(self, obj):
        # print('la salle de ce creneaux est:', obj.activity.salle)
        s_id = obj.activity.salle.id
        salle_name = obj.activity.salle.name
        # print('th eacti ', acti)
        # queryset = acti.salle.name
        # return SalleSerialiser(queryset, many=False).data
        return Response({'id': s_id, 'name': salle_name}).data

    def get_clients(self, obj):
        # abc = obj.abonnements.all()
        cr_id = obj.id
        clients = Client.objects.filter(abonnement_client__creneaux=obj)
        # print(clients)
        return ClientCreneauxSerializer(clients, many=True).data
        
    def get_clients_count(self, obj):
        # abc = obj.abonnements.all()
        cr_id = obj.id
        clients = Client.objects.filter(abonnement_client__creneaux=obj).count()
        # print(clients)
        # print('les client seont ', clients)
        return clients
        # client = Client.abonnement_client.all()
        # clients = abc.objects.filter(client=)
        # return ClientCreneauxSerializer(abc, many=True).data

        # clients = []
        # for client in abc :
        #     print('le client de labonnement', client.client)
        #     clients.append(client.client)
        # return clients.id
        # print('les clients de ce crenesaux',clients)
        # return ClientCreneauxSerializer(clients, many=True).data

    def get_activity_name(self, obj):
        return obj.activity.name



    # def get_presences(self, obj):
    #     query = obj.presenses.all()
    #     print('les preceses====>', obj.presenses.all())
    #     return PresenceSerialiser(query, many=True).data

# class CreneauClientSerialiser


class CreneauClientSerialiser(serializers.ModelSerializer):
    coach_name  = serializers.SerializerMethodField('get_coach_name', read_only=True)
    activity_name  = serializers.SerializerMethodField('get_activity_name', read_only=True)
    color       = serializers.CharField(source='coach.color', read_only=True)
    creneau_color       = serializers.SerializerMethodField('get_color', read_only=True)

    class Meta:
        model = Creneau
        fields = ('id', 'hour_start', 'hour_finish', 'day', 'activity_name', 'creneau_color', 'coach_name', 'coach', 'color')

    def get_color(self, obj):
        # print('la couleur ===>', obj.activity)
        return obj.get_color()
    def get_coach_name(self, obj):
        try:
            coach = obj.coach.first_name
        except:
            coach = False
        return coach
    def get_activity_name(self, obj):
        try:
            activity = obj.activity.name
        except:
            activity = False
        return activity


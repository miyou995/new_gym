from .models import Presence, PresenceCoach
from rest_framework import serializers
from creneau.models import Creneau
from abonnement.models import AbonnementClient
from client.models import Client
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)
now = datetime.now()
print(now, type(now))
class SimilarCreneauSerializer(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField('get_activity_name', read_only=True)
    class Meta:
        model = Creneau
        fields = ('id', 'activity')

    def get_activity_name(self, obj):
        return obj.activity.name

class PresenceHistorySerialiser(serializers.ModelSerializer):
    history_user_name = serializers.CharField(source= 'history_user')
    client = serializers.CharField(source = "abc.client")
    class Meta:
        model = Presence.history.model
        fields= "__all__"

class PresenceManualEditSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Presence
        # fields= ('id', )
        # exclude = ("abc","date","hour_entree", )
        fields= ("id",)
        # fields= "__all__"
        


#  presence manuelle non strict
class PresencePostSerialiser(serializers.ModelSerializer):
    # client = serializers.IntegerField(max_value=None, min_value=None, write_only=True)
    class Meta:
        model = Presence
        fields= ('id','creneau', 'hour_entree', 'hour_sortie', 'note', 'abc', 'date')

    def create(self, validated_data):
        abc = validated_data['abc']
        creneau = validated_data['creneau']
        presence_date = validated_data['date']
        hour_in = validated_data['hour_entree']
        hour_out = validated_data['hour_sortie']
        presence = Presence.objects.create(abc= abc, creneau= creneau, hour_entree=hour_in , hour_sortie=hour_out, date=presence_date)
        ecart = presence.get_time_consumed(hour_out)
        abc.presence_quantity -= ecart
        abc.save() 
        return presence
       


# presence auto NON - stricte ( souple )
class PresenceAutoSerialiser(serializers.ModelSerializer):

    # client_last_name = serializers.RelatedField(source='last_name', read_only=True)
    client = serializers.CharField(source = "abc.client")
    class Meta:
        model = Presence
        read_only_fields = ('creneau', 'hour_entree', 'hour_sortie')
        fields= ('client',)

    def create(self, validated_data):
        FTM = '%H:%M:%S'
        current_time = datetime.now().strftime("%H:%M:%S")
        cd_client = validated_data['abc']['client']
        try:
            client = Client.objects.get(Q(id=cd_client) | Q(carte=cd_client))
        except:
            card = cd_client.decode("utf-8")
            client = Client.objects.get(hex_card=card)
        # client.has_permission()
        creneaux = Creneau.range.get_creneaux_of_day().filter(abonnements__client=client).distinct()
        # print('Les creneaux of client=====>',Creneau.objects.filter(abonnements__client=client))
        print('creneaux du Today client=====>', creneaux)
        logger.warning('LOGLes creneaux du Today client=====-{}'.format(str(creneaux)))

        # print('CLIENT ID => ', client.id)
        # init_time = 1
        # the_creneau = ''
        if len(creneaux) :
            dur_ref_time_format = abs(datetime.strptime(str(creneaux[0].hour_start), FTM) - datetime.strptime(current_time, FTM))
            dur_ref= timedelta.total_seconds(dur_ref_time_format) 
            cren_ref = creneaux[0]
            for cr in creneaux:
                start = str(cr.hour_start)
                print('heure de début', start)
                temps = abs(datetime.strptime(start, FTM) - datetime.strptime(current_time, FTM))
                duree_seconde = timedelta.total_seconds(temps) 
                if dur_ref > duree_seconde:
                    dur_ref = duree_seconde
                    cren_ref = cr
            abon_list = AbonnementClient.objects.filter(client = client, end_date__gte=date.today(), archiver = False )
            if not abon_list:
                raise serializers.ValidationError("l'adherant n'est pas inscrit aujourd'hui")
            if len(abon_list) > 1:
                abon_list = abon_list.filter(creneaux = cren_ref)
            # creneaux = cren_ref,
            # end_date__gte=date.today(),
            print('ABON LIST', abon_list)
            for ab in abon_list: # si il y'a plusieurs abonnement on previlegie les abonnement normal vu qu'il ne sont pas recuperable
                # print("abonnement dans la bouvcle", ab.type_abonnement.free_sessions)
                if not ab.type_abonnement.free_sessions:
                    # if AbonnementClient.validity.is_valid(ab.id):
                    abonnement = ab
                else:
                    print('je suis laaaa')
                    abonnement = ab
            # abonnement = abon_list.first()
            # is_valid = AbonnementClient.validity.is_valid(abonnement.id)
            if abonnement.is_time_volume() and abonnement.presence_quantity > 30:
                print('IM HEEERE LOG ABONNEMENT==== TIME VOLUUUPME', abonnement.is_time_volume())
                presence = Presence.objects.create(abc= abonnement, creneau= cren_ref,  hour_entree=current_time )
                return presence

            if abonnement.presence_quantity > -2:
            # AbonnementClient.validity.is_valid(obj.id)
                presence = Presence.objects.create(abc= abonnement, creneau= cren_ref,  hour_entree=current_time )
                if abonnement.is_fixed_sessions() or abonnement.is_free_sessions():
                    abonnement.presence_quantity -= 1
                abonnement.save()
                return presence
            else:
                abonnement.presence_quantity
                logger.warning('LOG abonnement.presence_quantity=====> {}'.format(str(abonnement.presence_quantity)))
                logger.warning('LOG ABONNEMENT=====-{}'.format(str(abonnement)))
                logger.warning('LOG ABONNEMENT TYPE=====-{}'.format(str(abonnement.type_abonnement.type_of)))
                raise serializers.ValidationError("l'adherant n'est pas inscrit aujourd'hui")
        else:
            messages.error(self.request, "l'adherant n'est pas inscrit aujourd'hui")
            # raise serializers.ValidationError("l'adherant n'est pas inscrit aujourd'hui")
            return self
        # abonnement.update(presence_quantity = prenseces - 1 )

class PresenceEditSerialiser(serializers.ModelSerializer):
    client_last_name = serializers.RelatedField(source='last_name', read_only=True)
    class Meta:
        model = Presence
        read_only_fields = ('client_last_name', 'date', 'abc')
        fields= ('id','creneau', 'hour_sortie','client_last_name', 'abc', 'date', 'note')
        
    def update(self, instance, validate_data):
        current_time = datetime.now().strftime("%H:%M:%S")
        instance.hour_sortie = current_time
        print('lheure current_time ', current_time )
        entree = datetime.strptime(str(instance.hour_entree),"%H:%M:%S")
        sortie = datetime.strptime(str(current_time),"%H:%M:%S")
        # sortie = datetime.now().strftime("%H:%M:%S")
        print('lheure de hour_entree', entree)
        print('lheure de sortie', sortie)
        difference_secondes = (sortie - entree ).total_seconds()
        difference_minutes =  difference_secondes / 60
        # print('lheure de difference', difference.total_seconds() / 3600)
        abonnement = instance.abc
        if abonnement.is_time_volume():
            abonnement.presence_quantity -= difference_minutes
            abonnement.save()

        instance.save()
        return instance

class PresenceSerialiser(serializers.ModelSerializer):
    client_last_name = serializers.SerializerMethodField('get_client_name', read_only=True)
    activity = serializers.SerializerMethodField('get_activity', read_only=True)
    client = serializers.CharField(source="abc.client" , read_only=True)
    # dettes = serializers.SerializerMethodField('get_dettes_client', read_only=True)
    # dettes = serializers.CharField(source='abc.client.dettes', read_only=True)
    dettes = serializers.IntegerField(source='total_dette', read_only=True)

    seances = serializers.CharField(source='abc.get_quantity_str', read_only=True)
    is_red = serializers.CharField(source='abc.is_red', read_only=True)
    

    # quantity_str = serializers.CharField(source="abc.client" , read_only=True)
    class Meta:
        model = Presence
        fields= ('id', 'abc', 'creneau', 'client',  'client_last_name', 'note', 'hour_entree', 'hour_sortie', 'note', 'activity', 'date', 'seances', 'is_red', 'dettes')

    def get_client_name(self, obj):
        nom = f"{obj.abc.client.last_name} {obj.abc.client.first_name}"
        return nom

    def get_activity(self, obj):
        # print('abc', obj.creneau.planning)
        # print('GET ACTI', obj.creneau.activity)
        # activite = obj.creneau.activity.name
        try:
            # print('le type de lactivity', type(obj.creneau.activity), ' le je sais pas quoi',obj.creneau.activity)
            return obj.creneau.activity.name
        except:
            return False

    # def get_dettes_client(self, obj):
    #     # print('id ', obj.id)
    #     client_id = obj.abc.client
    #     try:
    #         dettes = AbonnementClient.objects.filter(client =client_id).aggregate(Sum('reste'))
    #     except:
    #         dettes = 0
    #     # print(dettes)
    #     return dettes


class PresenceClientSerialiser(serializers.ModelSerializer):
    client_activity = serializers.SerializerMethodField('get_activity', read_only=True)
    client_last_name = serializers.SerializerMethodField('get_client_name', read_only=True)
    client = serializers.CharField(source='abc.client.id', read_only=True)
    dettes = serializers.CharField(source='abc.client.dettes', read_only=True)
    abc_name = serializers.CharField(source='abc.type_abonnement', read_only=True)

    class Meta:
        model = Presence
        fields= ('id','abc','abc_name','client','creneau',  'hour_entree', 'dettes','hour_sortie', 'client_activity', 'client_last_name','date')


    def get_activity(self, obj):
        # activite = obj.creneau.activity.name
        try:
            return obj.creneau.activity.name
        except:

            return False
    def get_client_name(self, obj):
        nom = obj.abc.client.last_name
        # print('he hosdfvhnidso', nom) 
        return nom



    

class PresenceCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresenceCoach
        read_only_fields = ('date', 'hour_entree', 'hour_sortie')

        fields= ('coach', 'date', 'hour_entree', 'hour_sortie')  
    
    def create(self, validated_data):
        coach = validated_data['coach']
        current_time = now.strftime("%H:%M:%S")
        print('heure===============================', coach)
        presence = PresenceCoach.objects.create(coach= coach, hour_entree=current_time )
        return presence

    def update(self, instance, validated_data):
        current_time = now.strftime("%H:%M:%S")
        instance.hour_sortie = current_time
        instance.save()
        return instance
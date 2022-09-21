from .models import Presence, PresenceCoach
from rest_framework import serializers
from creneau.models import Creneau
from abonnement.models import AbonnementClient
from client.models import Client
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import Q
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
        fields= "__all__"
#  presence manuelle non strict
class PresencePostSerialiser(serializers.ModelSerializer):
    # client = serializers.IntegerField(max_value=None, min_value=None, write_only=True)
    class Meta:
        model = Presence
        fields= ('id','creneau', 'hour_entree', 'hour_sortie', 'note', 'abc', 'date')

    def create(self, validated_data):
        print('la premeire des choses ====>', validated_data)
        abc = validated_data['abc']
        creneau = validated_data['creneau']
        presence_date = validated_data['date']
        # print('CLIENT ID => ', client.id)
        # client_id = client.id
        client = Client.objects.get(abonnement_client__id=abc)
        # abonnement = AbonnementClient.objects.get(id=abc)
        # print('l \'abonnement du client est le :>>>>>>>>>>', abonnement)
        current_time = now.strftime("%H:%M:%S")
        he = current_time
        hour_in = validated_data['hour_entree']
        # prenseces = abon.presence_quantity 
        try:
            # THIS IS A SORTIE
            hour_out = validated_data['hour_sortie']
            presence = Presence.objects.create(abc= abc, creneau= creneau, hour_entree=hour_in , hour_sortie=hour_out,is_in_list=True, is_in_salle=False, date=presence_date)
            client.init_presence(dict(abc= abc, creneau= creneau, hour_in=hour_in , hour_sortie=hour_out,is_in_list=True, is_in_salle=False, date=presence_date))
            client.is_on_salle=False
            abc.presence_quantity -= 1 
        except :
            # THIS IS A ENTREE

            presence = Presence.objects.create(abc= abc, creneau= creneau, hour_entree=hour_in , is_in_list=True, is_in_salle=True, date=presence_date)
            abc.presence_quantity -= 1
            client.is_on_salle=True
        return presence
       
    # def create(self, validated_data):
    #     # creneaux_actuel = Creneau.range.get_creneau()
    #     # creneau = Creneau.range.get_creneau()[0]
    #     # print('validate ...................................data ', request)
    #     print('validate ::::::::::::::::::::::::::::::::::::::::::::::::::::data ', validated_data)
    #     client = validated_data['client']
    #     # client_id = client.id
    #     # abonnement = Client.abonnement_manager.get_abonnement(client)
    #     selected_abonnement = validated_data['abc']
    #     hour_in = validated_data['hour_entree']
    #     presence_date = validated_data['date']
    #     creneau = validated_data['creneau']
    #     # abc = AbonnementClient.objects.get(id=selected_abonnement)
    #     try:
    #         hour_out = validated_data['hour_sortie']
    #         presence = Presence.objects.create(abc= selected_abonnement, creneau= creneau, hour_entree=hour_in , hour_sortie=hour_out,is_in_list=True, is_in_salle=False, date=presence_date)
    #     except :
    #         presence = Presence.objects.create(abc= selected_abonnement, creneau= creneau, hour_entree=hour_in , is_in_list=True, is_in_salle=True, date=presence_date)
    #     selected_abonnement.presence_quantity -= 1 
    #     selected_abonnement.save() 
    #     print('presendvffdsbvfdsbvces ', selected_abonnement.presence_quantity)
    #     return presence

# presence auto NON - stricte ( souple )
class PresenceAutoSerialiser(serializers.ModelSerializer):
    # client_last_name = serializers.RelatedField(source='last_name', read_only=True)
    client = serializers.CharField(source = "abc.client")
    class Meta:
        model = Presence
        read_only_fields = ('creneau', 'is_in_list', 'hour_entree', 'hour_sortie', 'is_in_salle')
        fields= ('client',)
    

    def create(self, validated_data):
        FTM = '%H:%M:%S'
        current_time = datetime.now().strftime("%H:%M:%S")
        cd_client = validated_data['abc']['client']
        try:
            client = Client.objects.get(Q(id=cd_client) | Q(carte=cd_client  ))
        except:
            card = cd_client.decode("utf-8")
            client = Client.objects.get(hex_card=card)
        client.has_permission()
        creneaux = Creneau.range.get_creneaux_of_day().filter(abonnements__client=client)
        # print('Les creneaux of client=====>',Creneau.objects.filter(abonnements__client=client))
        print('Les creneaux du Today client=====>', creneaux)
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
            abon_list = AbonnementClient.objects.filter(client = client,creneaux = cren_ref, archiver = False )
            for ab in abon_list: # si il y'a plusieurs abonnement on previlegie les abonnement normal vu qu'il ne sont pas recuperable
                # print("abonnement dans la bouvcle", ab.type_abonnement.free_sessions)
                if not ab.type_abonnement.free_sessions:
                    # if AbonnementClient.validity.is_valid(ab.id):
                    abonnement = ab
                else:
                    print('je suis laaaa')
                    abonnement = ab
            # abonnement = abon_list.first()
            print('l \'abonnement du client est le :>>>>>>>>>>', abonnement)
            # is_valid = AbonnementClient.validity.is_valid(abonnement.id)
            if abonnement.is_time_volume() and abonnement.presence_quantity > 30:
                presence = Presence.objects.create(abc= abonnement, creneau= cren_ref, is_in_list=True, hour_entree=current_time, is_in_salle=True)
                return presence

            if abonnement.presence_quantity > -2:
            # AbonnementClient.validity.is_valid(obj.id)
                presence = Presence.objects.create(abc= abonnement, creneau= cren_ref, is_in_list=True, hour_entree=current_time, is_in_salle=True)
                if abonnement.is_fixed_sessions() or abonnement.is_free_sessions():
                    abonnement.presence_quantity -= 1
                abonnement.save()
                return presence
        else:
            raise serializers.ValidationError("l'adherant n'est pas inscrit aujourd'hui")
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

        instance.is_in_salle = False
        instance.save()
        return instance

class PresenceSerialiser(serializers.ModelSerializer):
    client_last_name = serializers.SerializerMethodField('get_client_name', read_only=True)
    activity = serializers.SerializerMethodField('get_activity', read_only=True)
    client = serializers.CharField(source="abc.client" , read_only=True)
    dettes = serializers.SerializerMethodField('get_dettes_client', read_only=True)
    seances = serializers.RelatedField(source='client.abonnement_client.presence_quantity', read_only=True)
    class Meta:
        model = Presence
        print('PresenceSerialiser')
        fields= ('id', 'abc', 'creneau', 'client', 'is_in_list', 'client_last_name', 'note', 'hour_entree', 'hour_sortie', 'is_in_salle', 'note', 'activity', 'date', 'seances', 'dettes')

    def get_client_name(self, obj):
        nom = f"{obj.abc.client.last_name} {obj.abc.client.first_name}"
        return nom

    def get_activity(self, obj):
        # activite = obj.creneau.activity.name
        try:
            print('le type de lactivity', type(obj.creneau.activity), ' le je sais pas quoi',obj.creneau.activity)
            return obj.creneau.activity.name
        except:
            return False

    # def get_similar_creneaux( self, obj):
    #     cren = []
    #     try:
    #         creneau_id = obj.creneau.id
    #         creneaux = Creneau.range.get_similar_creneaux(creneau_id)
    #         return SimilarCreneauSerializer(creneaux, many=True).data
    #     except:
    #         return cren
    def get_dettes_client(self, obj):
        # print('id ', obj.id)
        client_id = obj.abc.client
        try:
            dettes = AbonnementClient.objects.filter(client =client_id).aggregate(Sum('reste'))
        except:
            dettes = 0
        # print(dettes)
        return dettes


class PresenceClientSerialiser(serializers.ModelSerializer):
    client_activity = serializers.SerializerMethodField('get_activity', read_only=True)
    client_last_name = serializers.SerializerMethodField('get_client_name', read_only=True)
    client = serializers.CharField(source='abc.client.id', read_only=True)
    dettes = serializers.CharField(source='abc.client.dettes', read_only=True)
    abc_name = serializers.CharField(source='abc.type_abonnement', read_only=True)

    class Meta:
        model = Presence
        fields= ('id','abc','abc_name','client','creneau', 'is_in_list', 'hour_entree', 'dettes','hour_sortie', 'is_in_salle','client_activity', 'client_last_name','date')


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



#  presence automatique stricte
# class PresenceCreateSerialiser(serializers.ModelSerializer):
#     client_last_name = serializers.RelatedField(source='last_name', read_only=True)

#     class Meta:
#         model = Presence
#         read_only_fields = ('creneau', 'is_in_list','client_last_name', 'hour_entree', 'hour_sortie', 'is_in_salle')
#         fields= ('abc','client_last_name')
      

#     def create(self, validated_data):
#         print('la premeire des choses ====>', validated_data)
#         abc = validated_data['abc']
#         print('CLIENT ID => ', client.id)
#         client_id = client.id
#         abonnement = Client.abonnement_manager.get_abonnement(client_id)
#         print('l \'abonnement du client est le :>>>>>>>>>>', abonnement)

#         current_time = now.strftime("%H:%M:%S")
#         he = current_time

#         prenseces = abon.presence_quantity 
#         # print('ceci est labonnement du client ', abon)
#             # print('il est dans la liste')
#         presence = Presence.objects.create(abc= abc, creneau= creneau, hour_entree=he ,is_in_list=True, is_in_salle=True)
#         # abonnement = Client.abonnement_manager.get_abonnement(client_id)
#         # abonnement.update(presence_quantity -= 1 )
#         abon.presence_quantity -= 1
#         return presence
#         else:
#             print('le clients nest pas inscrit dans ce cours')

#     def update(self, instance, validate_data):
#         current_time = now.strftime("%H:%M:%S")
#         instance.hour_sortie = current_time
#         instance.is_in_salle = False
#         instance.save()
#         return instance
    

class PresenceCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresenceCoach
        read_only_fields = ('date', 'hour_entree', 'hour_sortie', 'is_in_salle')

        fields= ('coach', 'date', 'hour_entree', 'hour_sortie', 'is_in_salle')  
    
    def create(self, validated_data):
        coach = validated_data['coach']
        current_time = now.strftime("%H:%M:%S")
        print('heure===============================', coach)
        presence = PresenceCoach.objects.create(coach= coach, hour_entree=current_time , is_in_salle=True)
        return presence

    def update(self, instance, validated_data):
        current_time = now.strftime("%H:%M:%S")
        instance.hour_sortie = current_time
        instance.is_in_salle = False
        instance.save()
        return instance
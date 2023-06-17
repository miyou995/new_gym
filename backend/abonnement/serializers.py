
from salle_activite.models import Activity
from salle_activite.models import Salle
from .models import AbonnementClient, Abonnement
from rest_framework import serializers
from datetime import datetime, timedelta, date
from salle_activite.serializers import ActivitySerialiser, SalleSerialiser
from transaction.models import Paiement
from client.models import Client
from django.shortcuts import get_object_or_404

class PaiementClientSerializer(serializers.ModelSerializer):
    class Meta:
            model = Paiement
            fields= '__all__'

class AbonnementTestSerializer(serializers.ModelSerializer):
    class Meta:
            model = Abonnement
            fields= '__all__'

class ClientDropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
class AbonnementClientAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbonnementClient
        fields= '__all__'

class AbonnementClientHistorySerializer(serializers.ModelSerializer):
    left_minutes = serializers.SerializerMethodField('get_left_minutes', read_only=True)
    history_user_name = serializers.CharField(source= 'history_user')
    history_ab_type = serializers.CharField(source= 'type_abonnement.type_of')
    is_time_volume = serializers.SerializerMethodField()
    is_free_access = serializers.SerializerMethodField()
    is_fixed_sessions = serializers.SerializerMethodField()
    is_free_sessions = serializers.SerializerMethodField()
    # fixed_sessions = serializers.CharField(source= 'is_fixed_sessions')
    # free_sessions = serializers.CharField(source= 'is_free_sessions')
    # history_user_name = serializers.SerializerMethodField()
    class Meta:
        model = AbonnementClient.history.model
        # read_only_fields = ('client','start_date', 'end_date')
        # fields =('id', 'start_date','end_date', 'type_abonnement' , 'presence_quantity', 'reste', 'left_minutes', 'is_time_volume', 'is_free_access', 'is_fixed_sessions', 'is_free_sessions', 'history_user_name', 'history_ab_type')
        fields= '__all__'
        # fields= ('id','client','presence_quantity', 'history','creneaux','reste')
    def get_left_minutes(self, obj):
        minutes = obj.presence_quantity
        time = divmod(minutes, 60)
        # print('en heures', time)
        time_string = "{}H: {}M".format(time[0], time[1])
        # print('en time_string', time_string)
        return time_string

    def get_is_time_volume(self, obj):
        abc = get_object_or_404(AbonnementClient, id=obj.id)
        if abc.is_time_volume():
            return True
        else:
            return False
    def get_is_free_access(self, obj):
        abc = get_object_or_404(AbonnementClient, id=obj.id)
        if abc.is_free_access():
            return True
        else:
            return False
    def get_is_fixed_sessions(self, obj):
        abc = get_object_or_404(AbonnementClient, id=obj.id)
        if abc.is_fixed_sessions():
            return True
        else:
            return False
    def get_is_free_sessions(self, obj):
        abc = get_object_or_404(AbonnementClient, id=obj.id)
        if abc.is_free_sessions():
            return True
        else:
            return False

class AbonnementClientRenewSerializer(serializers.ModelSerializer):
    start_renew_date = serializers.CharField(write_only=True)
    abc = serializers.IntegerField(write_only=True)
    class Meta:
        model = AbonnementClient
        read_only_fields = ('client','start_date', 'abc','end_date')
        fields= ('id','client', 'abc', 'start_renew_date', 'presence_quantity', 'creneaux','reste')
    
    def create(self, validated_data):
        abc_id = validated_data['abc']
        start_renew_date = validated_data['start_renew_date']
        abc = AbonnementClient.objects.get(id=abc_id)
        abc_instance = abc.renew_abc(start_renew_date) 
        return abc_instance 

class AbonnementClientDetailUpdateSerialiser(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField('get_activity', read_only=True)
    type_abonnement = serializers.SerializerMethodField('get_abon_name', read_only=True)
    class Meta:
        model = AbonnementClient
        read_only_fields = ('client',)
        fields= ('id','start_date','end_date', 'client', 'type_abonnement', 'presence_quantity', 'creneaux', 'activity', 'reste')
        # depth= 4

    def get_activity(self, obj):
        abonnement_id = obj.type_abonnement.id
        print('abonnement_id TYPE', obj.type_abonnement.type_of)
        abonnement = Abonnement.objects.get(id = abonnement_id)
        salles = abonnement.salles.all() #ERRRRREEEEEEUUUUUUURRRRR
        activitesOfSalles=[] 
        for i in salles:
            print('ACTIVTIEES => ', i)
            act = Activity.objects.filter(salle_id = i)
            for j in act:
                lenght=len(activitesOfSalles)
                activitesOfSalles.insert(lenght,j)               
        print('---------------',activitesOfSalles)
            # actis= Salle.activites.all()
            # for j in actis:
            #     activitesOfSalles.insert(i)
            #     print(' ---------------------',j)
          
        return SalleSerialiser(activitesOfSalles, many=True).data
    def get_abon_name(self, obj):
        return obj.type_abonnement.name

class AbonnementClientSerialiser(serializers.ModelSerializer):
    # creneaux = serializers.PrimaryKeyRelatedField(many=True, queryset= Creneau.objects.all())
    # creneaux = CreneauSerialiser(many=True)
    type_abonnement_name = serializers.SerializerMethodField('get_abon_name', read_only=True)
    class Meta:
        model = AbonnementClient
        read_only_fields = ('presence_quantity',)
        fields= ('id','start_date', 'client', 'type_abonnement', 'presence_quantity', 'creneaux', 'type_abonnement_name')



    def get_abon_name(self, obj):
        return obj.type_abonnement.name

    def get_day_index(self, day):
        if day == 'DI':
            return 6
        elif day == 'LU':
            return 0
        elif day == 'MA':
            return 1
        elif day == 'ME':
            return 2
        elif day == 'JE':
            return 3
        elif day == 'VE':
            return 4
        elif day == 'SA':
            return 5
        else:
            return False
    def get_next_date(self, given_start_date, day):
        today = date.today()
        weekday = given_start_date.weekday()
        print('TODAY DE TODAY', day)
        the_next_day = given_start_date + timedelta((day-weekday) % 7)
        return the_next_day

    def create(self, validated_data):
        client = validated_data['client']
        creneaux = validated_data['creneaux']
        type_ab = validated_data['type_abonnement']
        start_date = validated_data['start_date']
        duree = type_ab.length
        duree_semaine = (duree // 7) - 1 
        selected_creneau= [cre.id for cre in creneaux]
        print('l-- selected_creneau ',selected_creneau)
        dates_array = []
        seances= type_ab.seances_quantity
        calculated_end_date = start_date + timedelta(days=duree)

        if type_ab.fixed_sessions():
            print('on the if')
            for creneau in creneaux :
                jour = self.get_day_index(creneau.day)
                next_date = self.get_next_date(start_date, jour)
                print(f'le prochain {creneau.day} in: {jour} est le {next_date}')
                dates_array.append(next_date)
            print('la MAX : ', max(dates_array))
            maxed_date = max(dates_array)
            calculated_end_date = maxed_date + timedelta(weeks=duree_semaine)
        elif type_ab.time_volume():
            seances= type_ab.seances_quantity * 60
        else:
            print('on the else')
            calculated_end_date = start_date + timedelta(days=duree)
        print('la calculated_end_date : ', calculated_end_date)
        abc_instance = AbonnementClient.objects.create(client= client, start_date= start_date ,end_date= calculated_end_date, type_abonnement = type_ab, presence_quantity=seances, reste=type_ab.price)
        for cren in selected_creneau:
            abc_instance.creneaux.add(cren)    
        abc_instance.save()
        return abc_instance 

        # for date in dates_array:
        #     print('date inividuelle : ', date)
            
    # def create(self, validated_data):
    #     print('validated_data =====>', validated_data)
    #     # return AbonnementClient.objects.create(**validated_data)
    #     abon = validated_data['type_abonnement']
    #     number = Abonnement.objects.get(id = abon.id).length
    #     delta = timedelta(days = number)
    #     end_date = datetime.now().date() + delta
    #     presence_quantity = Abonnement.objects.get(id = abon.id).seances_quantity

    #     abonnement_client = AbonnementClient.objects.create(end_date=end_date,presence_quantity=presence_quantity, **validated_data)
    #     return abonnement_client





        # abonnement_client.creneaux.create()
        # for creneau in creneaux:
        #     Creneau.objects.create(abonnements=abonnement_client, **creneaux)
        # for creneau in creneaux:
        #     Creneau.objects.create()
        
        
        # creneaux = validated_data['creneau']
        # client = validated_data['client']
        # abon = validated_data['type_abonnement']
        # print('presennnce =====>', presence_quantity)
        # return AbonnementClient.objects.create(end_date=end_date,presence_quantity=presence_quantity**validated_data)
class AbonnementClientDetailSerializer(serializers.ModelSerializer):
    # is_volume = serializers.BooleanField(source='is_time_volume')
    left_minutes = serializers.SerializerMethodField('get_left_minutes', read_only=True)
    type_abonnement_name = serializers.SerializerMethodField('get_type_abonnement_name', read_only=True)
    # cochage       = serializers.CharField(source='type_abonnement.systeme_cochage', read_only=True)
    price       = serializers.CharField(source='type_abonnement.price', read_only=True)
    class Meta:
        model = AbonnementClient
        fields =('id', 'start_date','end_date', 'type_abonnement' , 'type_abonnement_name','presence_quantity', 'creneaux',  'reste', 'price', 'left_minutes', 'is_time_volume', 'is_free_access', 'is_fixed_sessions', 'is_free_sessions', 'is_valid')

    def get_type_abonnement_name(self, obj):
        return obj.type_abonnement.name

    def get_left_minutes(self, obj):
        minutes = obj.presence_quantity
        time = divmod(minutes, 60)
        # print('en heures', time)
        time_string = "{}H: {}M".format(time[0], time[1])
        # print('en time_string', time_string)
        return time_string

class AbonnementSerialiser(serializers.ModelSerializer):   
    clients_number = serializers.SerializerMethodField('get_clients_number', read_only=True)
    salle_name = serializers.CharField(source='salles.name', read_only=True)
    class Meta:
        model = Abonnement
        read_only_fields = ('clients_number','salle_name')
        fields= ('id', 'name', 'price', 'type_of','length', 'seances_quantity', 'salles', 'clients_number','salle_name', 'type_of', 'actif')

    def get_clients_number(self, obj):
        try:
            queryset = Abonnement.objects.get(id = obj.id)
            number = queryset.type_abonnement_client.count()
            return number 
        except:
            return False
    
    # def get_activity_name(self, obj):
    #     try:
    #         return obj.activity.name
    #     except:
    #         return False

    # def create(self, validate_data):
    #     abon = Abonnement.objects.create(**validate_data)
    #     return True


class AbonnementClientTransactionsSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField('get_transactions', read_only=True)

    class Meta:
        model= AbonnementClient
        fields= ('client','type_abonnement','reste', 'transactions')
    def get_transactions(self, obj):
        trans = obj.transactions.all()
        return PaiementClientSerializer(trans, many=True).data

class ABCCreneauSerializer(serializers.ModelSerializer):
    abonnement = serializers.CharField(source='type_abonnement.name')
    client_data = serializers.SerializerMethodField('get_client_name', read_only=True)
    class Meta:
        model = AbonnementClient
        fields = ('id',  'client_data', 'start_date', 'end_date', 'reste', 'abonnement')
        # fields = '__all__'
    
    def get_client_name(self, obj):
        client= obj.client
        return ClientDropSerializer(client).data


    # def get_abonnement(self, obj):
    #     creneau = self.context['creneau']
    #     abonnement = AbonnementClient.objects.filter(id=obj.abonnement_client,creneaux=creneau)
    #     print('LA REQuETRTE',creneau)
    #     return AbonnementClientSerialiser(abonnement).data

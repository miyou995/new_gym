from rest_framework.fields import ReadOnlyField
from .models import Paiement, Autre, AssuranceTransaction, Remuneration, RemunerationProf, Transaction
from rest_framework import serializers
from rest_framework.response import Response

class PaiementSerialiser(serializers.ModelSerializer):
    # client = serializers.SerializerMethodField('abonnement_client.client', read_only=True)
    start_abc   = serializers.CharField(source='abonnement_client.start_date', read_only = True)
    end_abc     = serializers.CharField(source='abonnement_client.end_date', read_only = True)
    abonnement_name = serializers.CharField(source='abonnement_client.type_abonnement', read_only = True)
    client_last_name = serializers.CharField(source='abonnement_client.client.full_name', read_only=True)
    client_id = serializers.CharField(source='abonnement_client.client.id', read_only=True)
    abc_id = serializers.IntegerField(source='abonnement_client.id', read_only=True)
    quantity = serializers.CharField(source='abonnement_client.get_quantity_str', read_only=True)
    # get_abc_price = serializers.CharField(source='abonnement_client.price', read_only=True)

    class Meta:
        model = Paiement
        fields= ('id', 'amount', 'abonnement_client', 'last_modified', 'notes', 'abonnement_name', 'date_creation', 'client_last_name', 'client_id', 'abc_id', 'start_abc', 'end_abc', 'quantity', 'get_abc_price', 'get_abc_reste')


class PaiementFiltersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields= '__all__'
        
    # def get_client_name(self, obj):
    #     return Response({'id' : obj.client.id, 'name' : obj.client.last_name}).data

class PaiementPostSerialiser(serializers.ModelSerializer):
    abonnement_name = serializers.CharField(source='abonnement_client.type_abonnement', read_only = True)

    class Meta:
        model = Paiement
        fields= ('id', 'amount', 'abonnement_client', 'abonnement_name','last_modified', 'notes', 'date_creation')

    # def create(self, validated_data):
    #     print('yeeeee')
    #     return True
class RemunerationProfPostSerialiser(serializers.ModelSerializer):
    class Meta:
        model = RemunerationProf
        fields= ('id', 'amount', 'coach', 'last_modified', 'notes', 'date_creation')

class AssuranceSerialiser(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_client_name', read_only=True)

    class Meta:
        model = AssuranceTransaction
        fields= ('id', 'amount', 'client', 'last_modified', 'notes', 'date_creation')

    def get_client_name(self, obj):
        try:
            response = Response({'id' : obj.client.id, 'name' : obj.client.last_name}).data 
        except : 
            response = Response({'id' : "-", 'name' : '-'}).data 
        return response


class PaiementHistorySerialiser(serializers.ModelSerializer):
    history_user_name = serializers.CharField(source= 'history_user')
    client = serializers.SerializerMethodField('get_client_name', read_only=True)
    # client = serializers.CharField(source = "abonnement_client.client")
    class Meta:
        model = Paiement.history.model
        fields= "__all__"
    def get_client_name(self, obj):
        try:
           return obj.abonnement_client.client.full_name()
        except : 
            return 'null'
class AutreSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Autre
        fields= '__all__'

class AssurancePostSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AssuranceTransaction
        fields= '__all__'

class RemunerationSerialiser(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_client_name', read_only=True)
    class Meta:
        model = Remuneration 
        fields= ('id', 'amount', 'client', 'last_modified', 'notes', 'date_creation')

    def get_client_name(self, obj):
        return Response({'id' : obj.nom.id, 'name' : obj.nom.last_name}).data


class RemunerationPostSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Remuneration 
        fields= '__all__'

class RemunerationProfSerialiser(serializers.ModelSerializer):
    coach = serializers.SerializerMethodField('get_coach_name', read_only=True)

    class Meta:
        model = RemunerationProf
        fields= ('id', 'amount', 'coach', 'last_modified', 'notes', 'date_creation')
    def get_coach_name(self, obj):
        return Response({'id' : obj.coach.id, 'name' : obj.coach.last_name}).data


class TransactionSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields= '__all__'
        depth = 1
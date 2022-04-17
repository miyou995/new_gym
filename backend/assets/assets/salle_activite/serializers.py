from .models import Salle, Activity
from rest_framework import serializers
# from creneau.serializers import CreneauSerialiser

class SalleSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields= '__all__'

class ActivitySerialiser(serializers.ModelSerializer):
    salle_name = serializers.SerializerMethodField('get_salle_name', read_only=True)
    class Meta:
        model = Activity
        fields= ('id', 'name', 'color', 'salle', 'salle_name')

    def get_salle_name(self, obj):
        
        return obj.salle.name
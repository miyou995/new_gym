from .models import Planning
from rest_framework import serializers 
from salle_sport.serializers import SalleSportSerialiser, NameSalleSportSerialiser
from salle_sport.models import SalleSport



class PlanningSerialiser(serializers.ModelSerializer):
    # salle_name = serializers.SerializerMethodField('get_salle_name')

    class Meta:
        model = Planning
        # read_only_fields = ('salle_name',)
        fields= ('id', 'name', 'salle_sport', 'is_default')


    # def get_salle_name(self, obj):
    #     return obj.salle_sport.name
    
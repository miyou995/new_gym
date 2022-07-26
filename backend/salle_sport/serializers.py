from .models import SalleSport
from rest_framework import serializers
# from planning.serializers import PlanningSerialiser 

class SalleSportSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SalleSport
        fields= '__all__'


class NameSalleSportSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SalleSport
        fields= ('name',)

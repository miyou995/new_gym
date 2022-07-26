from .models import Materiel
from rest_framework import serializers


class MaterielSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Materiel
        fields= '__all__'

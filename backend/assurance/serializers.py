from .models import Assurance
from rest_framework import serializers


class AssuranceSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Assurance
        fields= '__all__'

from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Materiel
from .serializers import MaterielSerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated


class MaterielAPIView(generics.CreateAPIView):
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerialiser


class MaterielListAPIView(generics.ListAPIView):
    queryset = Materiel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MaterielSerialiser


class MaterielDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Materiel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MaterielSerialiser

    def get_object(self):
        obj = get_object_or_404(Materiel.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class MaterielDestroyAPIView(generics.DestroyAPIView):
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerialiser


    
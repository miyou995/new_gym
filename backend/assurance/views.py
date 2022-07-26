from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Assurance
from .serializers import AssuranceSerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated


class AssuranceAPIView(generics.CreateAPIView):
    queryset = Assurance.objects.all()
    serializer_class = AssuranceSerialiser



class AssuranceListAPIView(generics.ListAPIView):
    queryset = Assurance.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AssuranceSerialiser


class AssuranceDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Assurance.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = AssuranceSerialiser

    def get_object(self):
        obj = get_object_or_404(Assurance.objects.filter(id=self.kwargs["pk"]))
        return obj



class AssuranceDestroyAPIView(generics.DestroyAPIView):
    queryset = Assurance.objects.all()
    serializer_class = AssuranceSerialiser


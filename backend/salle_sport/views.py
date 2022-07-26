from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import SalleSport
from .serializers import SalleSportSerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated


class SalleSportAPIView(generics.CreateAPIView):
    queryset = SalleSport.objects.all()
    serializer_class = SalleSportSerialiser



class SalleSportListAPIView(generics.ListAPIView):
    queryset = SalleSport.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSportSerialiser


class SalleSportDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = SalleSport.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSportSerialiser

    def get_object(self):
        obj = get_object_or_404(SalleSport.objects.filter(id=self.kwargs["pk"]))
        return obj
    

class SalleSportDestroyAPIView(generics.DestroyAPIView):
    queryset = SalleSport.objects.all()
    serializer_class = SalleSportSerialiser


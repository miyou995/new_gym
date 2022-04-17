

from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Salle, Activity
from .serializers import SalleSerialiser, ActivitySerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework.decorators import api_view

class SalleAPIView(generics.CreateAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerialiser


class SalleListAPIView(generics.ListAPIView):
    queryset = Salle.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSerialiser


class SalleDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Salle.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = SalleSerialiser

    def get_object(self):
        obj = get_object_or_404(Salle.objects.filter(id=self.kwargs["pk"]))
        print('Salle ... ', obj , obj.id)
        return obj
    

class SalleDestroyAPIView(generics.DestroyAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerialiser


class ActivityAPIView(generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerialiser

    def post(self, request, format=None):
        print(request.data)
        serializer = ActivitySerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = 'Activité Creer avec succés'
            return Response({'success': msg}, status=status.HTTP_200_OK)
        else:
            msg = 'erreur : Activité non Creer'
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)



class ActivityListAPIView(generics.ListAPIView):
    queryset = Activity.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ActivitySerialiser


class ActivityDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Activity.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ActivitySerialiser

    def get_object(self):
        obj = get_object_or_404(Activity.objects.filter(id=self.kwargs["pk"]))
        print('ACTIVITé ', obj , obj.id)
        return obj
    

class ActivityDestroyAPIView(generics.DestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerialiser


@api_view(['GET'])
def presences_by_salle(request):
    salles = Salle.objects.values('name').annotate(Count('actvities__creneaux__presenses'))
    return Response( {'presences': salles})

@api_view(['GET'])
def default_salle(request):
    default_salle = Salle.custom_manager.default_salle()
    serializer = SalleSerialiser(default_salle, many=False)
    print('la samme', serializer.data)
    return Response( {'default_salle': serializer.data})
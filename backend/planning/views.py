from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Planning
from .serializers import PlanningSerialiser




class PlanningAPIView(generics.CreateAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerialiser

class PlanningListAPIView(generics.ListAPIView):
    queryset = Planning.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PlanningSerialiser


class PlanningDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Planning.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = PlanningSerialiser

    def get_object(self):
        obj = get_object_or_404(Planning.objects.filter(id=self.kwargs["pk"]))
        print('theeeeeeee ', obj , obj.id)
        return obj
    
    def put(self, request, *args, **kwargs):
        #  actuel = Planning.objects.get(pk = instance.id) 
        # plan = Planning.objects.update(salle_sport=request['salle_sport']['name'], name=request['name'])
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print("PATCHHHHHHHHH")
        return self.update(request, *args, **kwargs)


class PlanningDestroyAPIView(generics.DestroyAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerialiser


@api_view(['GET'])
def default_planning(request):
    planning = Planning.custom_manager.default_planning()
    serializer = PlanningSerialiser(planning, many=False)
    return Response( {'default_planning': serializer.data}) 
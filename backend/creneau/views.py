from django.shortcuts import render
from django.views.generic.base import TemplateView




class CreneauxView(TemplateView):
    template_name = "creneaux.html"
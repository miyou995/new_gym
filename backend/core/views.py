from django.shortcuts import render
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    print('=========== we are here')
    template_name = "index.html"

class ConfigurationView(TemplateView):   
    template_name = "configuration/configuration.html"
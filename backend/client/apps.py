from django.apps import AppConfig


class ClientConfig(AppConfig):
    name = 'client'
    
    # def ready(self):
    #     from . import signals
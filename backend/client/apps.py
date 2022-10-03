from django.apps import AppConfig


class ClientConfig(AppConfig):
    name = 'client'
    
    def read(self):
        print('im DONE APP CLIENT---------------------------------------------------------------------------------')
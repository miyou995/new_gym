from django.core.management.base import BaseCommand
from django.conf import settings
from salle_activite.tasks import ( 
    start_linsten_test_device_1, 
    start_linsten_test_device_2, 
    start_linsten_2,
    start_linsten_3, 
    start_linsten_4, 
    start_linsten_5, 
    start_linsten_6, 
    start_linsten_7,
    start_linsten_8, 
    start_linsten_9, 
    start_face_door_right, 
    start_face_door_left, 
)
from celery import group


class Command(BaseCommand):
    help = "after celery tasks being revoked at a certain time this command start them again"
    def add_arguments(self, parser):
        parser.add_argument(
            '--schema',
            action='store',
            dest='schema',
            help='Name of the tenant schema',
        )
    def handle(self, *args,**kwargs):
        if settings.DEBUG == True:
            group(
                start_linsten_test_device_1.delay(),
                start_linsten_test_device_2.delay(),
            )
        else:
            group(
                start_linsten_2.delay(),
                start_face_door_right.delay(),
                start_face_door_left.delay()
            )
        self.stdout.write('Gym open')
            
    

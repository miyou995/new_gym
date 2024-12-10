from django.core.management.base import BaseCommand
from django.utils import timezone
from abonnement.models import AbonnementClient
from presence.models import Presence
from datetime import date
from datetime import timedelta
from django.db.models import Q

class Command(BaseCommand):
    help = 'yesterday and today abc'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        today=date.today()

        abc_queryset = AbonnementClient.objects.filter(Q(start_date=today) | Q(start_date=yesterday))

        for abc in abc_queryset:
            if abc.type_abonnement.time_volume():
                print("abc_today--------------------", abc)
                presences = Presence.objects.filter(abc=abc)        
                print("presence------------------------", presences)
            else : 
                print("not time_volume ")
        





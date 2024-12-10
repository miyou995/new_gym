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

        abc_queryset = AbonnementClient.objects.filter(Q(start_date=yesterday))
        for abc in abc_queryset:
            if abc.type_abonnement.time_volume():
                print("abc_today--------------------", abc)
                base_reste = int(abc.type_abonnement.seances_quantity) * 60 
                last_presence = Presence.objects.filter(abc=abc).order_by('-created').first()
                print("presence------------------------", last_presence)
                if last_presence:
                    duration_minutes = last_presence.calculate_duration_minutes()
                    if duration_minutes:
                        if duration_minutes > 180:
                            abc.reste= base_reste - 180
                        else:
                            abc.reste = base_reste - duration_minutes
                        print("ecart------------------------", duration_minutes)
                    else:
                        print('not duration_minutes')
                        abc.reste = base_reste - 180
                else: 
                    abc.reste = base_reste
                abc.save()
                print("not time_volume ")
        self.stdout.write(self.style.SUCCESS('Successfully adjusted abc for yesterday and today clients'))
            


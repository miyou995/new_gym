from django.core.management.base import BaseCommand
from django.utils import timezone
from presence.models import Presence

class Command(BaseCommand):
    help = 'Set hour_sortie to 4:00 AM for presences where hour_sortie is null when the time is 5:00 AM'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        if now.hour == 5:
            # Set hour_sortie to exactly 4:00 AM for any Presence where hour_sortie is null
            four_am = now.replace(hour=4, minute=0, second=0, microsecond=0)
            presences_to_update = Presence.objects.filter(hour_sortie__isnull=True)

            for presence in presences_to_update:
                presence.hour_sortie = four_am.time()  # Set hour_sortie to 4:00 AM
                presence.save()

            self.stdout.write(self.style.SUCCESS('Successfully updated hour_sortie to 4:00 AM for presences where hour_sortie was null.'))
        else:
            self.stdout.write(self.style.WARNING('This command should only be run at 5:00 AM.'))
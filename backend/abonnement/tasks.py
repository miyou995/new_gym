
from celery import shared_task
from datetime import date
from .models import AbonnementClient


@shared_task
def auto_unlock_expired_locked_abc():

    qs = AbonnementClient.objects.filter(
        is_locked=True,
        lock_start_date__isnull=False,
        lock_duration_days__isnull=False,
    )

    for abc in qs:
        if abc.should_auto_unlock():
            abc.unlock()

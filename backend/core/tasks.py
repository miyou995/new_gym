
from celery import shared_task
from django.core.management import call_command


@shared_task
def dbbackup():

    call_command("dbbackup", "--clean", )

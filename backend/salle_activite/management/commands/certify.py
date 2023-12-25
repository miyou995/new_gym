import subprocess
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Issue SSL/TLS certificates using subprocess'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--domain', type=str, required=True,
                            help='The domain to issue the certificate for')

    def handle(self, *args, **options):
        domain = options['domain']
        www_domain = f"www.{domain}"
        password = settings.SG_PASS or "0000"

        command = [
            'sudo', '-S', 'certbot', '--nginx',
            '-d', domain,
            '-d', www_domain,
            '--redirect', '--non-interactive'
        ]

        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            stdout, stderr = process.communicate(input=f"{password}\n")

            # Log the output
            logger.info(stdout)
            if stderr:
                logger.error(stderr)

            if process.returncode != 0:
                raise CommandError(f'Failed to issue certificate for {domain}. Error: {stderr}')

        except Exception as e:
            logger.exception(f"Error while issuing certificate for {domain}: {e}")
            raise CommandError(f'Failed to issue certificate for {domain}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Successfully issued certificate for {domain}'))

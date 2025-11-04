import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings




class Command(BaseCommand):
    help = 'Restarts all the necessary services after pulling from the server'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting project restart process...'))

        self.stdout.write('Pull latest changes (optional, if not already done)...')

        self.run_command('git pull origin master')

        # Run migrations unless --no-migrate is specified
        if not options.get('no_migrate', False):
            self.stdout.write('Running database migrations...')
            self.run_command('python manage.py migrate')

        if not options.get('no_static', False):
            # Collect static files
            self.stdout.write('Collecting static files...')
            self.run_command('python manage.py collectstatic --noinput')

        # Clear cache
        self.stdout.write('Clearing cache...')
        self.run_command('python manage.py clear_cache')

        # Restart services (customize based on your project)
        self.stdout.write('Restarting services...')
        
        # Example: Restart Gunicorn (if used)
        self.run_command('sudo systemctl restart new_gym')
        self.stdout.write('Restarted Gunicorn service (new_gym) ')
        
        # Example: Restart Celery (if used)
        self.run_command('sudo systemctl restart celery')
        self.stdout.write('Restarted Celery worker (celery) ')
        self.run_command('sudo systemctl restart celery_beat')
        self.stdout.write('Restarted Celery beat worker (celery_beat) ')

        # Example: Restart Nginx (if used)
        self.run_command('sudo systemctl restart nginx')
        self.stdout.write('Restarted Nginx service (nginx) ')

        self.stdout.write(self.style.SUCCESS('Project restart completed successfully!'))

    def run_command(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error executing command: {command}'))
            self.stdout.write(self.style.ERROR(str(e)))
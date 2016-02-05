from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'set up this project'

    def handle(self, *args, **options):
        self.stdout.write('In expenses rebuild handle')
        management.call_command('zap_and_create_db', '--dropconnections')
        management.call_command('migrate')

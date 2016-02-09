from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings

import os


class Command(BaseCommand):
    help = 'set up this project'

    def handle(self, *args, **options):
        self.stdout.write('In expenses rebuild handle')
        management.call_command('zap_and_create_db', '--dropconnections')
        management.call_command('migrate')
        # Load users
        fixture_path = os.path.join(settings.BASE_DIR,
                                    'expenses_website/core/fixtures')
        file_path = os.path.join(fixture_path, 'app_users.json')
        management.call_command('loaddata', file_path)
        # Load categories
        file_path = os.path.join(fixture_path, 'app_categories.json')
        management.call_command('loaddata', file_path)

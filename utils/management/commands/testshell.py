from django.core.management.base import BaseCommand
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = 'Runs a Python interactive interpreter with test database and data from the given fixture(s).'
    args = '[fixture ...]'

    requires_model_validation = False

    def handle(self, *fixture_labels, **options):
        from django.core.management import call_command
        from django.db import connection
        
        verbosity = int(options.get('verbosity', 1))

        # Create a test database.
        db_name = connection.creation.create_test_db(verbosity=verbosity)

        # Import the fixture data into the test database.
        call_command('loaddata', *fixture_labels, **{'verbosity': verbosity})

        call_command('shell')

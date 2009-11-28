from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = "Runs the django test-runner, with the correct settings file."
    args = ""

    requires_model_validation = False

    def handle(self, *args, **options):
        from django.core.management import call_command
        settings.ON_TEST(settings)
        call_command('test', *args, **options)

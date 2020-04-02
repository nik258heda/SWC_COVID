from django.core.management.base import BaseCommand
from admin_panel.modelfactory import RequestFactory


class Command(BaseCommand):
    help = 'Seeds the database.'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            default=10,
                            type=int,
                            help='The number of fake objects to create.')

    def handle(self, *args, **options):
        for _ in range(options['number']):
            RequestFactory.create()

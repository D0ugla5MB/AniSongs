from sys import stdout
from django.core.management.base import BaseCommand, CommandError

from anisong.utils.format_data import export_formatter_func
from anisong.utils.files_config import get_anime_url_list

class Command(BaseCommand):
    help = "Run a specific formatter/exporter function by name."

    def add_arguments(self, parser):
        parser.add_argument(
            'function', 
            type=str, 
            help="Name of the exporter/formatter function to run."
        )

        parser.add_argument(
            'file', 
            nargs='+',
            type=str,
            help="Optional positional arguments for the formatter function."
        )
       
    def handle(self, *args, **options):
        func_name = options['function']
        func_args = options['file']
        try:
            func = export_formatter_func(func_name)
            func(*func_args)
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")

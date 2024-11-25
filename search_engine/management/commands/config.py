import inspect
import sys
from django.core.management.base import BaseCommand
from anisong.utils import files_config

class Command(BaseCommand):
    help = "Check if all required environment variables and configurations are set up correctly."

    def handle(self, *args, **kwargs):
        all_functions = inspect.getmembers(files_config, inspect.isfunction)
        getter_functions = {name: func for name, func in all_functions if name.startswith("get_")}

        for func_name, func in getter_functions.items():
            value = func()
            
            #check if the value is sensitive (e.g., contains 'client' in the name); lower_f to avoid caps lock stuff
            if 'client' in func_name.lower():
                value = "*********"  
            
            if not value: 
                self.stdout.write(self.style.ERROR(f"{func_name}: MISSING or EMPTY"))
                sys.exit(1)  
            else:
                self.stdout.write(self.style.SUCCESS(f"{func_name}: OK - {value}"))

        self.stdout.write(self.style.SUCCESS("All environment variables are ready to use!"))

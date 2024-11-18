import os
import json
import re
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Copies a JSON file, extracts numbers from the URL path, and saves the modified JSON'

    def handle(self, *args, **kwargs):
        input_partial_path = "search_engine/output.json"
        input_full_path = os.path.join(settings.BASE_DIR, input_partial_path)

        if not os.path.exists(input_full_path):
            self.stdout.write(self.style.ERROR(f"File not found: {input_full_path}"))
            return

        try:
            with open(input_full_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if not isinstance(data, (list, dict)):
                self.stdout.write(self.style.ERROR("Expected JSON to be a list or dictionary."))
                return

            def process_item(item):
                if isinstance(item, dict) and "url" in item:
                    url = item["url"]
                    match = re.search(r'/anime/(\d+)/', url)
                    if match:
                        item["extracted_numbers"] = [match.group(1)]
                    else:
                        item["extracted_numbers"] = []
                return item

            if isinstance(data, list):
                processed_data = [process_item(item) for item in data]
            else:
                processed_data = process_item(data)

            output_partial_path = "search_engine/output_copy.json"
            output_full_path = os.path.join(settings.BASE_DIR, output_partial_path)

            with open(output_full_path, 'w', encoding='utf-8') as file:
                json.dump(processed_data, file, indent=4)

            self.stdout.write(self.style.SUCCESS(f"Copied and modified JSON saved to: {output_full_path}"))

        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing file: {e}"))

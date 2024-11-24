import json
import os
from django.core.management.base import BaseCommand
from anisong.utils.files_config import get_template_json, get_utils_dir


class Command(BaseCommand):
    help = 'Generate JSON files for anime track lists based on template'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            help='Directory where the generated JSON files will be saved',
            default=get_utils_dir(),  
        )
        parser.add_argument(
            '--data-file',
            type=str,
            help='Path to the JSON file containing data sets',
            default=None,  
        )

    def handle(self, *args, **kwargs):
        output_dir = kwargs['output_dir']
        data_file = kwargs['data_file']
        template_file = get_template_json()  
        data_sets = None
        
        if data_file:
            if not os.path.exists(data_file):
                self.stdout.write(self.style.WARNING(f"Warning: The file '{data_file}' does not exist."))
                return
            if os.path.getsize(data_file) == 0:
                self.stdout.write(self.style.WARNING(f"Warning: The file '{data_file}' is empty."))
                return
            with open(data_file, "r") as file:
                try:
                    data_sets = json.load(file)
                except json.JSONDecodeError:
                    self.stdout.write(self.style.WARNING(f"Warning: The file '{data_file}' is not a valid JSON."))
                    return
        else:
            # Default data_sets in case no file is provided
            data_sets = [
                {
                    "type_track_list": "opening",
                    "anime_id": 1234,
                    "name": "Example Anime 1",
                    "myanimelist_url": "anime_url_anime_1",
                    "track_list": [
                        {"track_name": "Song 1", "artist_name": "Artist 1", "track_id": "track_001", "artist_id": "artist_001"}
                    ]
                },
                {
                    "type_track_list": "ending",
                    "anime_id": 5678,
                    "name": "Example Anime 2",
                    "myanimelist_url": "anime_url_anime_2",
                    "track_list": [
                        {"track_name": "Song 2", "artist_name": "Artist 2", "track_id": "track_002", "artist_id": "artist_002"},
                        {"track_name": "Song 3", "artist_name": "Artist 3", "track_id": "track_003", "artist_id": "artist_003"}
                    ]
                },
            ]

        with open(template_file, "r") as file:
            json_template = json.load(file)

        def create_json(type_track_list, anime_id, name, myanimelist_url, track_list):
            json_data = json_template.copy()
            
            json_data["type_track_list"] = type_track_list
            json_data["anime_id"] = anime_id
            json_data["anime_info"]["name"] = name
            json_data["anime_info"]["myanimelist_url"] = myanimelist_url
            json_data["anime_info"]["track_list"] = track_list
            
            return json_data

        for i, data in enumerate(data_sets):
            populated_json = create_json(
                data["type_track_list"],
                data["anime_id"],
                data["name"],
                data["myanimelist_url"],
                data["track_list"]
            )
            
            file_name = os.path.join(output_dir, f"{data['type_track_list']}_{data['anime_id']}.json")

            with open(file_name, "w") as file:
                json.dump(populated_json, file, indent=4)

            self.stdout.write(self.style.SUCCESS(f"Generated {file_name}"))

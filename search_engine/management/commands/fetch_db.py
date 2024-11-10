import csv
import os
import warnings
from django.core.management.base import BaseCommand, CommandError
from search_engine.models import Song, Anime, Artist

def check_warning_RightData():
        file = 'right_data.csv'

        if not os.path.exists(file):
            warnings.warn(
                f"Required file '{file}' is missing. Please create or add this file before running the script.",
                UserWarning
            )
        else:
            if os.path.getsize(file) == 0:
                warnings.warn(
                    f"File '{file}' exists but is empty. Please ensure it has data.",
                    UserWarning
                )
            else:
                try:
                    with open(file, newline='', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        headers = next(reader, None)
                        
                        if headers is None:
                            warnings.warn(
                                f"File '{file}' exists but appears not to be in valid CSV format. Please check the file content.",
                                UserWarning
                            )
                        else:
                            print(f"File '{file}' is present, not empty, and in CSV format.")
                except Exception as e:
                    warnings.warn(
                        f"File '{file}' could not be read as a CSV file. Error: {str(e)}",
                        UserWarning
                    )


class Command(BaseCommand):
    help = 'Save data on song\'s database from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', 
            type=str, 
            help='The file path to the CSV file with song data.'
        )

    def handle(self, *args, **options):
        check_warning_RightData()
        
        file_path = options['file_name']

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    anime_title = row.get('anime')
                    artist_name = row.get('artist')
                    song_type = row.get('song_type')
                    song_name_roman = row.get('song_name_roman')
                    song_name_jp = row.get('song_name_jp', '')

                    anime = Anime.objects.get(default_title=anime_title)
                    artist = Artist.objects.get(name=artist_name)

                    song, created = Song.objects.update_or_create(
                        anime=anime,
                        song_name_roman=song_name_roman,
                        defaults={
                            'song_type': song_type,
                            'song_name_jp': song_name_jp,
                            'artist': artist
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created new song: {song_name_roman}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated existing song: {song_name_roman}'))

        except FileNotFoundError:
            raise CommandError(f"File '{file_path}' does not exist.")
        except Anime.DoesNotExist:
            raise CommandError(f"Anime '{anime_title}' does not exist in the database.")
        except Artist.DoesNotExist:
            raise CommandError(f"Artist '{artist_name}' does not exist in the database.")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
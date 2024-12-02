from django.core.management import BaseCommand, call_command

from anisong.utils.files_config import get_anime_url_list

class Command(BaseCommand):
    help = 'Function to save the animes\'songs data to the database (models)\n'
    
    def handle(self, *args, **options):
        """
        call_command('fetch_mal_data')
        call_command('fetch_anime_songs')
        call_command('spotify_data_search')
        call_command('fetch_db') 
        """
        call_command('format_data_files', 'anime_index', get_anime_url_list())
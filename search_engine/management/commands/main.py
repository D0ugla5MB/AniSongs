from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = 'Function to save the animes\'songs data to the database (models)\n'
    
    def handle(self, *args, **options):
        call_command('fetch_mal_data')
        call_command('fetch_anime_songs')
        call_command('spotify_data_search')
        call_command('fetch_db')
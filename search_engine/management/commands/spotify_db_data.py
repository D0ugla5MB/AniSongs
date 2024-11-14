import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.core.management.base import BaseCommand, CommandError
    
    
load_dotenv()

class Command(BaseCommand):
    help='Spotify data to populate the database'
    
        
    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Search for Spotify artists\'id')

    def handle(self, *args, **options):
        q = options['query']
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR("SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET must be set in the environment."))
            return
        
        spot = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

        results = spot.search(q, 10, 0, 'album', 'BR')

        for idx, item in enumerate(results['albums']['items']):
            artist_name = item['artists'][0]['name']  
            album_name = item['name']
            self.stdout.write(f"{idx + 1}. Artist: {artist_name}\tAlbum: {album_name}")

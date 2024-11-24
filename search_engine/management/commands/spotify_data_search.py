from collections import deque
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Searches playlists and processes tracks using Spotipy"

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help="Search term for playlists")
        
    def handle(self, *args, **options):
        q = options['query']
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR("SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET must be set in the environment."))
            return
        
        spot = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

        playlists = spot.search(q=q, type='playlist', limit=5, market='BR')  
        queue = deque()
        
        for playlist in playlists['playlists']['items']:
                playlist_id = playlist['id']
                playlist_name = playlist['name']
                queue.append((playlist_id, playlist_name))
    
        while queue:
            playlist_id, playlist_name = queue.popleft()
            self.stdout.write(f"\nProcessing playlist: {playlist_name} (ID: {playlist_id})")
            playlist_tracks = spot.playlist_tracks(playlist_id)
            
            for item in playlist_tracks['items']:
                track = item['track']
                if track:  
                    track_name = track['name']
                    artists = ', '.join(artist['name'] for artist in track['artists'])
                    self.stdout.write(f"  - Track: {track_name}, Artist(s): {artists}")
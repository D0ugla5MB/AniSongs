ENABLE_TO_RUN = False

if ENABLE_TO_RUN:
    import requests
    import os
    from dotenv import load_dotenv
    from django.core.management.base import BaseCommand
    import secrets

    load_dotenv()

    AUTH_URL = "https://myanimelist.net/v1/oauth2/authorize"
    TOKEN_URL = "https://myanimelist.net/v1/oauth2/token"

    class Command(BaseCommand):
        help = "Fetch anime data from MyAnimeList API using OAuth 2.0"

        def add_arguments(self, parser):
            parser.add_argument(
                '--query', type=str, required=True,
                help="Search query for anime (e.g., 'one')"
            )
            parser.add_argument(
                '--limit', type=int, default=100,
                help="Number of results to fetch (default: 4)"
            )

        def handle(self, *args, **options):
            query = options['query']
            limit = options['limit']
            
            client_id = os.getenv('MAL_CLIENT_ID')
            client_secret = os.getenv('MAL_CLIENT_SECRET')
            redirect_uri = os.getenv('MAL_REDIRECT_URI')

            if not client_id or not client_secret or not redirect_uri:
                self.stderr.write("Error: Missing Client ID, Client Secret, or Redirect URI in .env.")
                return

            access_token = os.getenv('MAL_ACCESS_TOKEN')

            if not access_token:
                self.stdout.write("No access token found. Starting the authorization flow.")
                
                code_verifier = self.generate_code_verifier()
                code_challenge = code_verifier  # plain method uses the verifier as the challenge
                authorization_code = self.get_authorization_code(client_id, code_challenge, redirect_uri)

                if not authorization_code:
                    self.stderr.write("Error: Failed to obtain authorization code.")
                    return

                access_token = self.get_access_token(client_id, client_secret, authorization_code, code_verifier, redirect_uri)
                
                if not access_token:
                    self.stderr.write("Error: Failed to obtain access token.")
                    return

                self.stdout.write(f"Access token obtained: {access_token}")
            
            self.fetch_anime_data(query, limit, access_token)


        def generate_code_verifier(self):
            """Generate a code verifier for PKCE."""
            code_verifier = secrets.token_urlsafe(100)[:128]
            self.stdout.write(f"Generated code verifier: {code_verifier}")
            return code_verifier

        def get_authorization_code(self, client_id, code_challenge, redirect_uri):
            """Direct the user to the authorization URL and get the code."""
            auth_url = (
                f"{AUTH_URL}?response_type=code"
                f"&client_id={client_id}"
                f"&code_challenge={code_challenge}"
                f"&code_challenge_method=plain"
                f"&redirect_uri={redirect_uri}"
            )

            self.stdout.write("Visit the following URL to authorize the app:")
            self.stdout.write(auth_url)
            authorization_code = input("Enter the authorization code: ").strip()
            return authorization_code

        def get_access_token(self, client_id, client_secret, code, code_verifier, redirect_uri):
            """Exchange the authorization code for an access token."""
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "code_verifier": code_verifier,
                "redirect_uri": redirect_uri,
            }

            try:
                response = requests.post(TOKEN_URL, data=data)
                response.raise_for_status()
                token_data = response.json()
                access_token = token_data.get("access_token")
                self.stdout.write(f"Access token obtained: {access_token}")
                return access_token
            except requests.exceptions.RequestException as e:
                self.stderr.write(f"Error obtaining access token: {e}")
                return None

        def fetch_anime_data(self, query, limit, access_token):
            """Fetch anime data from the MyAnimeList API."""
            url = f"https://api.myanimelist.net/v2/anime?q={query}&limit={limit}"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                self.stdout.write("Anime Data Fetched Successfully:")
                self.stdout.write(str(data))
            except requests.exceptions.RequestException as e:
                self.stderr.write(f"Error fetching data: {e}")
else:
    import sys 
    
    sys.exit("\033[91mThis script is DISABLED\033[0m")
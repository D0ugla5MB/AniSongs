import os
from dotenv import load_dotenv
from anisong import settings


MY_UTILS_DIR = os.getenv("MY_UTILS_DIR")
UTILS_BASE_DIR = MY_UTILS_DIR if MY_UTILS_DIR else os.path.join(settings.BASE_DIR, "utils")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
TEMPLATE_JSON_PATH = os.getenv("TEMPLATE_FILE_PATH")
SCRAPY_ID_NAME = os.getenv("SCRAPY_ID_NAME")
SCRAPY_DOMAIN_NAME = os.getenv("SCRAPY_DOMAIN_NAME")
SCRAPY_MALSPIDER_URL_SELECTOR = "table div > h3 > a"
SCRAPY_ANIME_SPIDER_ID_NAME = 'anime_op_ed'
MAL_ANIME_URL_BASE = 'https://myanimelist.net/topanime.php?type=tv&limit='

def get_scrapy_anime_spider_id_name() -> str:
    return SCRAPY_ANIME_SPIDER_ID_NAME

def get_mal_anime_url_base() -> str:
    return MAL_ANIME_URL_BASE

def get_scrapy_malspider_url_selector() -> str:
    return SCRAPY_MALSPIDER_URL_SELECTOR

def get_scrapy_id_name() -> str:
    return SCRAPY_ID_NAME

def get_scrapy_domain_name() -> str:
    return SCRAPY_DOMAIN_NAME

def get_anime_url_list() -> str:
    return os.path.join(UTILS_BASE_DIR, 'animes_url_list.json')

def get_anime_song_list() -> str:
    return os.path.join(UTILS_BASE_DIR, 'anime_op_ed.json')

def get_song_list_data() -> str:
    return os.path.join(UTILS_BASE_DIR, 'songs_data.json')

def get_spotify_client_secret() -> str:
    return SPOTIPY_CLIENT_SECRET

def get_spotify_client_id() -> str:
    return SPOTIPY_CLIENT_ID

def get_spotify_redirect_uri() -> str:
    return SPOTIPY_REDIRECT_URI

def get_template_json() -> str:
    return TEMPLATE_JSON_PATH

def get_utils_dir() -> str:
    return MY_UTILS_DIR
import os
from dotenv import load_dotenv

load_dotenv()

UTILS_BASE_DIR = os.getenv('MY_UTILS_DIR')
TEMPLATE_JSON_PATH = os.getenv('TEMPLATE_FILE_PATH')

def get_anime_url_list() -> str:
    return os.path.join(UTILS_BASE_DIR, 'animes_url_list.json')

def get_anime_song_list() -> str:
    return os.path.join(UTILS_BASE_DIR, 'anime_op_ed.json')

def get_song_list_data() -> str:
    return os.path.join(UTILS_BASE_DIR, 'songs_data.json')

def get_template_json() -> str:
    return TEMPLATE_JSON_PATH

def get_utils_dir() -> str:
    return UTILS_BASE_DIR 
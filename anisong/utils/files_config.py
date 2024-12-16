import os
import pdb
import re
from anisong import settings

MY_UTILS_DIR = os.getenv("MY_UTILS_DIR")
UTILS_BASE_DIR = MY_UTILS_DIR if MY_UTILS_DIR else os.path.join(settings.BASE_DIR, "utils")
JSON_FILES_DIR = os.getenv('JSON_FILES_DIR')
#######################################################################
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
#######################################################################
SCRAPY_PROJECT_DIR_BASE = os.getenv('SCRAPY_DIR_BASE')
SCRAPY_ID_NAME = os.getenv("SCRAPY_ID_NAME")
SCRAPY_DOMAIN_NAME = os.getenv("SCRAPY_DOMAIN_NAME")
SCRAPY_MALSPIDER_URL_SELECTOR = "table div > h3 > a"
SCRAPY_ANIME_SPIDER_ID_NAME = 'anime_op_ed'
SCRAPPY_CSS_SELECTORS = {
    "anime_title": "//h1/strong/text()",
    "op": "opnening",
    "ed": "ending",
    "sections_xpath": "//div[contains(@class, 'opnening') or contains(@class, 'ending')]",
    "td_xpath": ".//td[@width='84%']",
    "jp_text_css": '//span[@class="dark_text" and text()="Japanese:"]/following-sibling::text()'
}

#######################################################################
JSON_TEMPLATE = {
        "anime":{
            "anime_myanimelist_id":"",
            "anime_roman_title": "",
            "anime_jp_title": "",
        },
        "song":{
            "num": "",
            "roman_name": "",
            "jp_name": "",
            "type": "",
        },
        "artist":{
            "roman_name": "",
            "jp_name": "",
        },
        "spotify":{
            "song_id":"",
            "artist_id":"",
        }
    }

MAL_ANIME_URL_BASE = 'https://myanimelist.net/topanime.php?type=tv&limit='
MAL_URLs_BY_TYPE = {
    'tv': 'https://myanimelist.net/topanime.php?type=tv&limit=',
    'movie': 'https://myanimelist.net/topanime.php?type=movie&limit=',
    'ova': 'https://myanimelist.net/topanime.php?type=ova&limit=',
    'ona': 'https://myanimelist.net/topanime.php?type=ona&limit=',
    'special': 'https://myanimelist.net/topanime.php?type=special&limit=',
    'all': 'https://myanimelist.net/topanime.php?limit=',
    'upcoming': 'https://myanimelist.net/topanime.php?type=upcoming&limit=0',
}
#######################################################################
TEMPLATE_JSON_PATH = os.getenv("TEMPLATE_FILE_PATH")
ANIMES_URL_LIST = os.getenv('ANIMES_URL_LIST_PATH')
ANIME_OP_ED_PATH = os.getenv('ANIME_OP_ED_PATH')
SONGS_DATA_PATH = os.getenv('SONGS_DATA_PATH')
#######################################################################
REGEX_PATTERNS = {
    'mal_id_url': re.compile(r'/anime/(\d+)/'),
    'num': re.compile(r'(?:(\d+):\s*)?'),
    'song_name': re.compile(r'"(.*?)"'),
    'artist_name': re.compile(r'\s+by\s+(.+?)'),
    'extra_info_par': re.compile(r'(?:\s*\((.*)\))?'),
    'extra_info_bracket': re.compile(r'(?:\s*\[(.*?)\])?$'),
    'by_breaker': re.compile(r'\sby\s'),   
    'jp_txt': re.compile(r'[\u3000-\u9FFF]+'),
    'swap': re.compile(r'[\)\"\(\]\[]'),
    'placeholder': re.compile(r'§')
}
PLACEHOLDERS = ['§', '¬']
SYMBOLS_FOR_REGEX = [r'[:\)\"\(\]\[]', r'by']
#######################################################################__END__###

def pause_coderun(): pdb.set_trace()

def get_css_selectors(): return SCRAPPY_CSS_SELECTORS

def get_json_template(): return JSON_TEMPLATE

def get_regex_patterns(): return REGEX_PATTERNS

def get_placeholders(): return PLACEHOLDERS


def select_directory_path(dir_name): return {
        'aux_files': settings.AUXILIAR_FILES_DIR,
        'json': settings.JSON_FILES_DIR,
    }.get(dir_name, settings.BASE_DIR)

def select_mal_url(anime_type): return MAL_URLs_BY_TYPE.get(anime_type, "Invalid type")

def get_scrapy_location() -> str: return SCRAPY_PROJECT_DIR_BASE

def get_scrapy_anime_spider_id_name() -> str: return SCRAPY_ANIME_SPIDER_ID_NAME

def get_mal_anime_url_base() -> str: return MAL_ANIME_URL_BASE

def get_scrapy_malspider_url_selector() -> str: return SCRAPY_MALSPIDER_URL_SELECTOR

def get_scrapy_id_name() -> str: return SCRAPY_ID_NAME

def get_scrapy_domain_name() -> str: return SCRAPY_DOMAIN_NAME

def get_anime_url_list() -> str: return ANIMES_URL_LIST

def get_anime_song_list() -> str: return ANIME_OP_ED_PATH

def get_song_list_data() -> str: return SONGS_DATA_PATH

def get_spotify_client_secret() -> str: return SPOTIPY_CLIENT_SECRET

def get_spotify_client_id() -> str: return SPOTIPY_CLIENT_ID

def get_spotify_redirect_uri() -> str: return SPOTIPY_REDIRECT_URI

def get_template_json() -> str: return TEMPLATE_JSON_PATH

def get_utils_dir() -> str: return MY_UTILS_DIR
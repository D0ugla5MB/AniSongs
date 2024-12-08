import json
import re
from anisong.utils.files_config import get_placeholders, get_regex_delimiters, pause_coderun

def save_delimiter():
    v = None
    def fr(p):
        nonlocal v
        v = p
        return v
    return fr

def verify_by_word(inp_str, by_delim, ph):
    match = re.search(by_delim, inp_str)
    
    if match:
        start, end = match.span()
        new_str = inp_str[:start] + ph + inp_str[end:]
        return new_str
    
    return inp_str

def put_placeholders(input_str, placehold=get_placeholders, delimiters=get_regex_delimiters):
    delimiter = save_delimiter()
    has_num ,hasnot_num = placehold()
    spe_ch_delimit, by_delimit = [re.compile(pat) for pat in delimiters()]
    
    regex_ph = has_num if re.search(r'^\d+', input_str) else hasnot_num 
    aux_str = ''.join(verify_by_word(input_str, by_delimit, regex_ph))
    
    result_str = []
    result_str = [regex_ph] * (regex_ph == has_num) #not skip the num part to avoid to compute the num.seq. afterwards
    
    for i in range(len(aux_str)):
        if spe_ch_delimit.search(aux_str[i]):
            result_str.append(regex_ph)
        else:
            result_str.append(aux_str[i])
    

    modified_str = ''.join(result_str)
    pause_coderun()    
    return [modified_str, delimiter(regex_ph)]
 
def extract_substrings(pre_data):
    preformated_str, re_delimiter = pre_data
    matched_substr = []
    n = len(preformated_str)
    i, j = 0, 0  

    while i < n:

        while i < n and preformated_str[i] != re_delimiter:
            i += 1
        j = i + 1
        while j < n and preformated_str[j] != re_delimiter:
            j += 1

        if i < n and j < n and j - i > 1:
            matched_substr.append(preformated_str[i + 1:j])  

        i = j + 1
    
    return matched_substr
 
def extract_index_data(url_files):
    with open(url_files, 'r', encoding='utf-8') as f:
      url_files = json.load(f)
    formatted_data = []
    for anime in url_files:
        anime_data = {
            "anime_id": anime.get("anime_id"),
            "anime_name": anime.get("anime_title")
        }
        formatted_data.append(anime_data)

    with open('anime_data.json', 'w') as f:
        json.dump(formatted_data,fp=f, indent=4)
    print("Anime data saved to anime_data.json.")

def extract_song_data(songs_file, anime_id, anime_name):
    with open(songs_file, 'r', encoding='utf-8') as f:
      songs_file = json.load(f)
    
    formatted_data = {
        "anime_id": anime_id,
        "anime_info": {
            "name": anime_name,
            "track_list": []
        }
    }

    for song in songs_file:
        track_data = {
            "type_track_list": song.get("content_type"),
            "track_name": song.get("text_content").split('\"')[1],
            "artist_name": song.get("text_content").split('by ')[1].split(' (')[0],
            "track_id": song.get("text_content").split('\"')[0].split(':')[0],
            "artist_id": song.get("text_content").split('by ')[1].split(' (')[0]
        }
        formatted_data["anime_info"]["track_list"].append(track_data)

    with open('songs_data.json', 'w', encoding='utf-8') as f:
        json.dump([formatted_data], f, ensure_ascii=False, indent=4)
    print("Song data saved to songs_data.json.")

def export_formatter_func(func_name):
    func_exporter = {
        'anime_index': extract_index_data,
        'song_data': extract_song_data
    }
    return func_exporter.get(func_name)
import json

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
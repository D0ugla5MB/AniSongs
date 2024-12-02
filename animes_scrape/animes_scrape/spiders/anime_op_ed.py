import scrapy
import re
import json

from anisong.utils.files_config import (
    get_anime_url_list,
    get_scrapy_anime_spider_id_name,
    select_json_template,
)

class AnimeOpEdSpider(scrapy.Spider):
    name = get_scrapy_anime_spider_id_name()
    input_file = get_anime_url_list()
    json_template = select_json_template('data')
        
    def start_requests(self):
        try:
            with open(self.input_file, "r") as f:
                anime_data = json.load(f)
        except FileNotFoundError:
            self.log(f"Input file '{self.input_file}' not found.")
            return

        for anime in anime_data:
            anime_url = anime.get("anime_url")
            if anime_url:
                yield scrapy.Request(url=anime_url, callback=self.parse_anime)
            else:
                self.log(f"No URL found for anime: {anime}")
    
    def parse_anime(self, response):

        href_match = re.search(r'/anime/(\d+)/', response.url)
        anime_id = href_match.group(1) if href_match else None
        anime_title = response.xpath("//h1/strong/text()").get()

        track_list = []
        sections = response.xpath("//div[contains(@class, 'opnening') or contains(@class, 'ending')]")
        for section in sections:
            is_opening = "opnening" in section.get().lower()
            type_track_list = "opening" if is_opening else "ending"
            td_elements = section.xpath(".//td[@width='84%']")
            for td in td_elements:
                track_content = td.xpath("string(.)").get()
                by_index = track_content.find(' by ')

                if by_index != -1:
                    left_part = track_content[:by_index].strip()

                    colon_index = left_part.find(':')

                    if colon_index != -1:
                        track_id = left_part[:colon_index].strip()
                        track_name = left_part[colon_index + 1:].strip()
                        track_name = track_name.strip('"')

                    artist_content = track_content[by_index + 4:].strip()

                    extra_info = ""
                    episode_info_match = re.search(r'\(eps [^)]*\)', artist_content)
                    if episode_info_match:
                        extra_info = episode_info_match.group(0).strip('()')  
                        artist_content = artist_content.replace(episode_info_match.group(0), "").strip()

                    artist_name = artist_content.strip()

                    spotify_data = {
                        "spotify_artist_id": "",  
                        "spotify_track_id": "" 
                    }
                    
                    track_list.append({
                        "type_track_list": type_track_list,
                        "track_name": track_name.strip() if track_name else "",  
                        "artist_name": artist_name.strip() if artist_name else "",  
                        "extra_info": extra_info.strip() if extra_info else "",  
                        "track_id": track_id.strip() if track_id else "",  
                        "spotify_data": spotify_data,
                    })
                        
        anime_data = {
            "anime_id": int(anime_id) if anime_id else "",
            "anime_info": {
                "name": anime_title.strip() if anime_title else "",
                "track_list": track_list,
            }
        }

        yield anime_data

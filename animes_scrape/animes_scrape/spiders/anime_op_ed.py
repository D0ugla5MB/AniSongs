import logging
import scrapy
import re
import json
from anisong.utils.format_data import (extract_substrings)
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
        anime_id = ""
        anime_title = ""
        track_list = []
        type_track_list = ""
        track_name = ""
        artist_name = ""
        extra_info = ""
        track_id = ""

        href_match = re.search(r'/anime/(\d+)/', response.url)
        anime_id = href_match.group(1) if href_match else None
        anime_title = response.xpath("//h1/strong/text()").get()

        sections = response.xpath("//div[contains(@class, 'opnening') or contains(@class, 'ending')]")
        for section in sections:
            is_opening = "opnening" in section.get().lower()
            type_track_list = "opening" if is_opening else "ending"
            td_elements = section.xpath(".//td[@width='84%']")
            for td in td_elements:
                track_content = td.xpath("string(.)").get()
                self.log(f"[DEBUG] Raw track content: {track_content}", level=logging.DEBUG)
                
                if track_content:
                    extracted_data = extract_substrings(track_content)

                    if extracted_data:
                        self.log(f"\033[36m[DEBUG]\033[0m Raw track content: {track_content}", level=logging.DEBUG)
                        track_id = extracted_data[0] if len(extracted_data) > 0 else ""
                        track_name = extracted_data[1] if len(extracted_data) > 1 else ""
                        artist_name = extracted_data[2] if len(extracted_data) > 2 else ""
                        extra_info = " ".join(extracted_data[3:]) if len(extracted_data) > 3 else ""
                    else:
                        self.log(f"\033[31m[ERROR]\033[0m Invalid data extracted: {extracted_data}", level=logging.ERROR)

                    spotify_data = {"spotify_artist_id": "", "spotify_track_id": ""}
                    track_list.append({
                        "type_track_list": type_track_list,
                        "track_name": track_name.strip(),
                        "artist_name": artist_name.strip(),
                        "extra_info": extra_info.strip(),
                        "track_id": track_id.strip(),
                        "spotify_data": spotify_data,
                    })
                else:
                    self.log(f"\033[33m[WARNING]\033[0m Empty track content found", level=logging.WARNING)


        anime_data = {
            "anime_id": int(anime_id) if anime_id else "",
            "anime_info": {
                "name": anime_title.strip() if anime_title else "",
                "track_list": track_list,
            }
        }
        self.log(f"\033[32m[SUCCESS]\033[0m Parsed data for anime ID: {anime_id}")
        yield anime_data

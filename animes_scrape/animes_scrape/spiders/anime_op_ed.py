import logging
import scrapy
import re
import json
from anisong.utils.format_data import (extract_substrings, put_placeholders)
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
                yield scrapy.Request(url=anime_url, callback=self.scrape_anime_song_data)
            else:
                self.log(f"No URL found for anime: {anime}")
    
    def scrape_anime_song_data(self, response):
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
                
                if track_content:
                    extracted_data = extract_substrings(track_content)
                    
        yield {
            "anime_id": anime_id,
            "anime_info": {
                "anime_title": anime_title,
                "tracklist_info":{ #pre formatted data just from down here
                    "track_list": track_list,
                    "type_track_list": type_track_list,
                    "track_name": track_name,
                    "artist_name": artist_name,
                    "extra_info": extra_info,
                    "track_id": track_id
                }
            }
        }
import scrapy
import re
import json
from anisong.utils.format_data import (extract_substrings, put_placeholders)
from anisong.utils.files_config import (
    pause_coderun,
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
        op_list = []
        ed_list = []
        tracklist_type = ""

        href_match = re.search(r'/anime/(\d+)/', response.url)
        anime_id = href_match.group(1) if href_match else None
        anime_title = response.xpath("//h1/strong/text()").get()

        sections = response.xpath("//div[contains(@class, 'opnening') or contains(@class, 'ending')]")
        for section in sections:
            is_opening = "opnening" in section.get().lower()
            tracklist_type = "opening" if is_opening else "ending"
            td_elements = section.xpath(".//td[@width='84%']")
            for td in td_elements:
                
                track_content = ''.join(td.xpath("string(.)").get().split())
                
                if not track_content:
                    self.logger.error(f"Error at '\033[92m'track_content'\033[0m' extraction for anime: {anime_title}, song data is missing.")
                    continue

                try:
                    prepared_data  = put_placeholders(track_content)
                    extracted_data = extract_substrings(prepared_data)
                    if not all(extracted_data):
                        self.logger.error(f"Error at extracted_data for anime: {anime_title}, '\033[92m'extracted data'\033[0m': {extracted_data} is invalid.")
                        continue

                    track_data = {
                        "track_id": extracted_data[0] if extracted_data[0] not in [None, ''] else 'empty',
                        "track_name": extracted_data[1] if extracted_data[1] not in [None, ''] else 'empty',
                        "artist_name": extracted_data[2] if extracted_data[2] not in [None, ''] else 'empty',
                        "extra_info": extracted_data[3] if extracted_data[3] not in [None, ''] else 'empty'
                    }

                    if not track_data["track_id"]:
                        self.logger.error(f"Error at '\033[92m'track_data'\033[0m' construction for anime: {anime_title}, missing track_id in {track_data}.")
                        continue

                except Exception as e:
                    self.logger.error(f"Error processing song data for anime: {anime_title}, song content: {track_content}, error: {str(e)}")
                    continue

                if tracklist_type == "opening":
                    try:
                        op_list.append(track_data)
                    except Exception as e:
                        self.logger.error(f"Error appending to '\033[92mop_list\033[0m' for anime: {anime_title}, track_data: {track_data}, error: {str(e)}")
                else:
                    try:
                        ed_list.append(track_data)
                    except Exception as e:
                        self.logger.error(f"Error appending to '\033[92med_list\033[0m' for anime: {anime_title}, track_data: {track_data}, error: {str(e)}")

        try:
            yield {
                "anime_id": anime_id,
                "anime_info": {
                    "anime_title": anime_title,
                    "tracklist": {
                        "openings": op_list,
                        "endings": ed_list,
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error during yield for anime: {anime_title}, error: {str(e)}")
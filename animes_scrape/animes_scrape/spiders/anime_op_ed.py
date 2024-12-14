import scrapy
import re
import json
from anisong.utils.format_data import (extract_substrings, parse_song_info, put_placeholders, trim_trailing_spaces)
from anisong.utils.files_config import (
    get_css_selectors,
    get_json_template,
    get_regex_patterns,
    pause_coderun,
    get_anime_url_list,
    get_scrapy_anime_spider_id_name,
)

class AnimeOpEdSpider(scrapy.Spider):
    name = get_scrapy_anime_spider_id_name()
    input_file = get_anime_url_list()
    json_template_pros = get_json_template()
    
    def start_requests(self):
        try:
            with open(self.input_file, "r") as f:
                anime_data = json.load(f)
        except FileNotFoundError:
            self.log(f"Input file '{self.input_file}' not found.")
            return
        except json.JSONDecodeError:
            self.log(f"Error decoding JSON in the input file '{self.input_file}'.")
            return

        if not anime_data:  
            self.log(f"Input file '{self.input_file}' is empty.")
            return
        
        for anime in anime_data:
            anime_url = anime.get("anime_url")
            if anime_url:
                self.log(f"Processing URL: {anime_url}")
                yield scrapy.Request(url=anime_url, callback=self.scrape_anime_song_data)
            else:
                self.log(f"No URL found for anime entry: {anime}")
    
    def scrape_anime_song_data(self, response):
        json_template = get_json_template()
        anime = json_template["anime"]
        song = json_template["song"]
        artist = json_template["artist"]
        spotify = json_template["spotify"]
        op_list = []
        ed_list = []
        
        css_selectos = get_css_selectors()
        regex_patterns = get_regex_patterns()
        

        href_match = regex_patterns.get('mal_id_url').search(response.url).group(1)
        anime['anime_myanimelist_id'] = href_match if href_match else '-1'
        anime['anime_roman_title'] = response.xpath(css_selectos.get('anime_title')).get()
        anime['anime_jp_title'] = response.xpath(css_selectos.get('jp_text_css')).get()
        
        sections = response.xpath(css_selectos.get('sections_xpath'))
        for section in sections:
            is_opening = css_selectos.get('op') in section.get().lower()
            song['type'] = "opening" if is_opening else "ending"
            td_elements = section.xpath(css_selectos.get('td_xpath'))
            for td in td_elements:
                #new_str = trim_trailing_spaces(td.xpath("string(.)").get())
                track_content = trim_trailing_spaces(td.xpath("string(.)").get())
                #pause_coderun()
                track_content = parse_song_info(regex_patterns, track_content)
                if not track_content:
                    self.logger.error(f"Error at '\033[92m'track_content'\033[0m' extraction for anime: {anime['anime_roman_title']}, song data is missing.")
                    continue

                try:
                    song_data = track_content['song']
                    artist_data = track_content['artist']
                    
                    song['num'], song['roman_name'], song['jp_name'] = song_data
                    artist['roman_name'], artist['jp_name'] = artist_data
                    track_data = {'song': song, 'artist': artist}
                    
                 #   pause_coderun()
                    if song['type'] == "opening":
                            try:
                                op_list.append(track_data)
                            except Exception as e:
                                self.logger.error(f"Error appending to 'op_list' for anime: {anime['anime_roman_title']}, {track_data}, error: {str(e)}")
                    else:
                            try:
                                ed_list.append(track_data)
                            except Exception as e:
                                self.logger.error(f"Error appending to 'ed_list' for anime: {anime['anime_roman_title']}, track_data: {track_data}, error: {str(e)}")

                except Exception as e:
                    self.logger.error(f"Error processing song data for anime: {anime['anime_roman_title']}, song content: {track_content}, error: {str(e)}")
                    continue
        try:
            yield {
                "anime": anime,
                "openings": op_list,
                "endings": ed_list, 
                "spotify": spotify,
            }
        except Exception as e:
            self.logger.error(f"Error during yield for anime: {anime['anime_roman_title']}, error: {str(e)}")
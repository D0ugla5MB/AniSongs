import scrapy
import json

from anisong.utils.files_config import get_anime_song_list, get_scrapy_anime_spider_id_name

class AnimeOpEdSpider(scrapy.Spider):
    name = get_scrapy_anime_spider_id_name()
    input_file = get_anime_song_list()

    def start_requests(self):
        try:
            with open(self.input_file, "r") as f:
                anime_data = json.load(f)
 
        except FileNotFoundError:
            self.log(f"Input file '{self.input_file}' not found.")
 
            return

        for anime in anime_data:
            url = anime.get("url")
 
            if url:
                yield scrapy.Request(url=url, callback=self.parse_anime)
            else:
                self.log(f"No URL found for anime: {anime}")

    def parse_anime(self, response):
        sections = response.xpath("//div[contains(@class, 'opnening') or contains(@class, 'ending')]")
 
        for section in sections:
            td_elements = section.xpath(".//td[@width='84%']")
            for td in td_elements:
                text_content = td.xpath("string(.)").get()  
                yield {
                    "content_type": "opening" if "opnening" in section.get() else "ending",
                    "text_content": text_content.strip() if text_content else None,
                }

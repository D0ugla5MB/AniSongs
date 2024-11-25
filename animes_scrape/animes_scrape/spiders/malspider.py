import re
import scrapy

from anisong.utils.files_config import get_mal_anime_url_base, get_scrapy_domain_name, get_scrapy_id_name, get_scrapy_malspider_url_selector

class MalspiderSpider(scrapy.Spider):
    name = get_scrapy_id_name()
    allowed_domains = [get_scrapy_domain_name()]
    css_selector = get_scrapy_malspider_url_selector()
    num_limit = 0
    start_urls = [f"{get_mal_anime_url_base()}{num_limit}"]

    def parse(self, response):
        links = response.css(self.css_selector)
        if not links:
            self.log("Stopping crawl: No 'div > h3 > a' tags found.")
            return

        for link in links:
            href = link.attrib.get("href")
            anchor_text = link.xpath("text()").get()
            path_number = (match.group(1) if (match := re.search(r'/anime/(\d+)/', href)) else None)
            yield {
                "anime_url": href,
                "anime_title": anchor_text,
                "anime_id" :path_number,
            }

        page_title = response.xpath("//title/text()").get()
        if "4" in page_title:
            self.log("Stopping crawl: <title> tag contains '4'.")
            return

        self.num_limit += 50
        next_page = f"{get_mal_anime_url_base()}{self.num_limit}"

        if self.num_limit == 100:
            return

        yield scrapy.Request(url=next_page, callback=self.parse)

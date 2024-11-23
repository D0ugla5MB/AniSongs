import re
import scrapy

class MalspiderSpider(scrapy.Spider):
    name = "myanimelist"
    allowed_domains = ["myanimelist.net"]
    num_limit = 0
    start_urls = [f"https://myanimelist.net/topanime.php?type=tv&limit={num_limit}"]

    def parse(self, response):
        links = response.css("table div > h3 > a")
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
        next_page = f"https://myanimelist.net/topanime.php?type=tv&limit={self.num_limit}"

        if self.num_limit == 100:
            return

        yield scrapy.Request(url=next_page, callback=self.parse)

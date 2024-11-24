import os
import sys
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from anisong.utils.files_config import get_anime_url_list


class Command(BaseCommand):
    help = "Run the myanimelist Scrapy spider and save the output to a JSON file."

    def handle(self, *args, **kwargs):
        
        scrapy_project_path = os.path.join(os.getcwd(), "animes_scrape")
        sys.path.append(scrapy_project_path)
        self.stdout.write("Starting Scrapy spider...")

        feeds_key = get_anime_url_list()
        settings = get_project_settings()
        settings.update(
            {
                "FEEDS": {  
                    feeds_key: {"format": "json", "overwrite": True},
                }
            }
        )

        from animes_scrape.spiders.malspider import MalspiderSpider
        process = CrawlerProcess(settings)
        process.crawl(MalspiderSpider)
        process.start()  

        self.stdout.write(self.style.SUCCESS("Spider finished. Output saved to output.json."))

import os
import sys
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from anisong.utils.files_config import get_anime_url_list, get_scrapy_location


class Command(BaseCommand):
    help = "Run the myanimelist Scrapy spider and save the output to a JSON file."

    def handle(self, *args, **kwargs):
        
        scrapy_project_path = os.path.join(os.getcwd(), get_scrapy_location())
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

        from animes_scrape.animes_scrape.spiders.malspider import MalspiderSpider # type: ignore
        process = CrawlerProcess(settings)
        process.crawl(MalspiderSpider)
        process.start()  

        self.stdout.write(self.style.SUCCESS(f"Spider finished. Output saved {feeds_key}"))

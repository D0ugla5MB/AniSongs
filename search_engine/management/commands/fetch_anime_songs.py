import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand

from animes_scrape.animes_scrape.spiders.anime_op_ed import AnimeOpEdSpider # type: ignore
from anisong.utils.files_config import get_anime_song_list # type: ignore

class Command(BaseCommand):
    help = "Run the anime_op_end Scrapy spider and save the output to a JSON file."

    def handle(self, *args, **kwargs):
        file_path = get_anime_song_list()

        settings = get_project_settings()
        settings.update({
            'FEEDS': {
                file_path: {  
                    'format': 'json',  
                    'overwrite': True,
                    'indent': 2,  
                },
            },
            'FEED_EXPORT_INDENT': 2,
        })

        process = CrawlerProcess(settings)
        process.crawl(AnimeOpEdSpider)
        process.start()  

        self.stdout.write(self.style.SUCCESS('Spider has finished running!'))

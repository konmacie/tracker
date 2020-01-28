from django.core.management.base import BaseCommand
from services.models import Service, Post, ScraperRunLog
from services import scrapers
from django.utils import timezone


class Command(BaseCommand):
    help = 'Run scrapers for active services'

    def get_scraper_class(self, scraper_type):
        if scraper_type == Service.SCRAPPER_REDDIT:
            return scrapers.RedditScraper
        if scraper_type == Service.SCRAPPER_RSS:
            return scrapers.RssScraper

    def handle(self, *args, **options):
        services = Service.objects.filter(active=True)
        run_log = ScraperRunLog.objects.create()

        for service in services:
            scraper_class = self.get_scraper_class(service.scraper)
            scraper = scraper_class(service, run_log)
            print("Running scraper for: {}".format(str(service)))
            scraper.get_new_posts()
            scraper.save_new_posts()

            run_log.status = ScraperRunLog.STATUS_FINISHED
            run_log.timestamp_end = timezone.now()
            run_log.save()

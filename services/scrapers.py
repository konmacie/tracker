import requests
from bs4 import BeautifulSoup
import logging
from services.models import Post
from django.utils.html import escape
from django.utils import timezone

logger = logging.getLogger(__name__)


class AbstractScraper():
    def __init__(self, service, run_log):
        self.headers = {'User-agent': 'tracker/0.1'}
        self.posts = []
        self.service = service
        self.run_log = run_log

    def get_new_posts(self):
        raise NotImplementedError

    def save_new_posts(self):
        try:
            for post in reversed(self.posts):
                new_post, created = Post.objects.get_or_create(
                    service=self.service,
                    guid=post['guid']
                )
                if created:
                    new_post.title = post['title']
                    new_post.author = post['author']
                    new_post.url = post['url']
                    new_post.description = post['description']
                    new_post.run_log = self.run_log
                    new_post.save()

            self.service.last_run = timezone.now()
            self.service.save()
        except Exception:
            logger.exception('An error occured in: save_new_posts')


class RedditScraper(AbstractScraper):

    def get_new_posts(self):
        try:
            url = self.service.url
            url_parts = url.split('?')
            url_parts[0] = "{}.json".format(url_parts[0])
            url = "?".join(url_parts)

            r = requests.get(url, headers=self.headers)
            result = r.json()

            children = result['data']['children']
            for child in children:
                post_data = child['data']
                post_url = "https://www.reddit.com{}".format(
                    post_data['permalink'])
                post = {
                    'title': post_data['title'],
                    'guid': post_data['permalink'],
                    'author': post_data['author'],
                    'url': post_url,
                    'description': '',
                }
                self.posts.append(post)
        except Exception:
            logger.exception(
                'An error occured in: RedditScraper.get_new_posts')


class RssScraper(AbstractScraper):

    def get_new_posts(self):
        try:
            r = requests.get(self.service.url, headers=self.headers)
            soup = BeautifulSoup(r.content, 'xml')
            items = soup.find_all('item')
            for item in items:
                post = {
                    'title': None,
                    'url': None,
                    'description': '',
                    'author': '',
                    'guid': None,
                }
                post['title'] = escape(item.title.text)
                post['url'] = escape(item.link.text)
                post['guid'] = escape(item.guid.text)
                if item.description:
                    post['description'] = escape(item.description.text)
                if item.author:
                    post['author'] = escape(item.author.text)
                self.posts.append(post)

        except Exception:
            logger.exception(
                'An error occured in: RssScraper.get_new_posts')

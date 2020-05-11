import sys
import yaml
from urllib.parse import urlparse

from bs4 import BeautifulSoup

import logging
import argparse

import requests
import requests_cache

logging.getLogger().setLevel(logging.INFO)

class SiteException(Exception):
    pass

class Site(object):
    headers = {"user-agent": "The Coolest Useragent"}

    html = ""

    def __init__(self, url, *args, **kwargs):
        self.url = url

        try:
            self.html = requests.get(self.url, headers=self.headers).text
        except requests.exceptions.ConnectionError as e:
            logging.error("Failed to request %s: %s", url, e)
        if self.html:
            self.soup = BeautifulSoup(self.html, 'html.parser')
            super().__init__(*args, **kwargs)
        else:
            raise SiteException

    @property
    def feedSoup(self):
        result = []
        # print(self.soup('head'))
        for link in self.soup('link'):
            if 'type' in link.attrs and (
                'application/rss' in link['type'] or
                'application/atom' in link['type']
            ):
                result.append({
                    'title': link.get('title', None),
                    'href': link['href'],
                    'type': link['type']
                })
        return result

    @property
    def title(self):
        if self.soup("title"):
            return u''.join(self.soup.title.string)

    @property
    def og(self):
        result = {}
        for property in ('type', 'title', 'url', 'image'):
            og = self.soup.find("meta",  property="og:%s" % (property))
            result[property] = og['content'] if og else None
        return result

    def __dict__(self):
        return {
            'url': str(self.url),
            'detail': {
                'title': self.title,
                'feeds': self.feedSoup,
                'og': self.og
            }
        }

    def __str__(self):
        return str(self.__dict__())


class Feed(object):
    def __init__(self, site):
        self.urls = ['href' in site.feedSoup]


class Feed(object):
    def __init__(self, href):
        self.feed = feedparser.parse(href)
#        'feed': 147,
#        'entries': 147,
#        'bozo': 147,
#        'headers': 147,
#        'href': 147,
#        'status': 147,
#        'encoding': 147,
#        'version': 147,
#        'namespaces': 147,
#        'etag': 113,
#        'updated': 113,
#        'updated_parsed': 113,
#        'bozo_exception': 6


def SiteList(filename):
    """
    List all Sites in README.md

    .. todo::
        Sort and filter dupes.
    """
    with open(filename) as urls:
        sitereader = yaml.load(urls, Loader=yaml.SafeLoader)
        for site in sitereader['Websites']:
            logging.error(site)
            yield site


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--topic',
                        dest='topic',
                        default='README.md',
                        help='Input topic to process.')
    parser.add_argument('--output',
                        dest='output',
                        default="sites.yaml",
                        help="""GCS Path of the output file
                        including filename prefix.""")
    websites = []
    requests_cache.install_cache('cache')

    known_args, pipeline_args = parser.parse_known_args(sys.argv)

    for site in SiteList(known_args.topic):
        try:
            url = urlparse(site['Link']).geturl()
        except Exception as e:
            logging.error(e)

        if url:
            try:
                site = Site(url)
                print(site)
            except SiteException:
                continue

    sys.exit()

    with open(known_args.output, "w") as y:
        y.write(yaml.safe_dump(websites, default_flow_style=False))

    for site in websites:
        for feed in site['detail']['feeds']:
            if feed['href'].startswith("http"):
                print(feed['href'])
            else:
                print("%s%s" % (site['url'], feed['href']))

    sys.exit(0)

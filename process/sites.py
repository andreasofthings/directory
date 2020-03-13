import sys
import yaml
import requests
import requests_cache

from bs4 import BeautifulSoup

import logging
import argparse

logging.getLogger().setLevel(logging.INFO)

class SiteException(Exception):
    pass

class Site(object):
    headers = {"user-agent": "The Coolest Useragent"}

    html = ""

    def __init__(self, url, *args, **kwargs):

        try:
            self.html = requests.get(url, headers=self.headers).text
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
            'url': str(url),
            'detail': {
                'title': self.title,
                'feeds': self.feedSoup,
                'og': self.og
            }
        }


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


def URLlist(filename):
    """
    List all URLs in urls.yaml

    .. todo::
        Sort and filter dupes.
    """
    from urllib.parse import urlparse
    with open(filename) as urls:
        urlreader = yaml.load(urls)
        for url in urlreader['Websites']:
            logging.error(url)
            yield urlparse(url['Link']).geturl()


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

    for url in URLlist(known_args.topic):
        try:
            site = Site(url)
        except SiteException:
            continue

        try:
            websites.append(site.__dict__())
        except Exception as e:
            print("EXCEPTION: ", e)
            # print(e)
            # print(websites[-1])
            # print(type(websites[-1]))

    with open(known_args.output, "w") as y:
        y.write(yaml.safe_dump(websites, default_flow_style=False))

    for site in websites:
        for feed in site['detail']['feeds']:
            if feed['href'].startswith("http"):
                print(feed['href'])
            else:
                print("%s%s" % (site['url'], feed['href']))

    sys.exit(0)

import sys
import csv
import yaml
import requests
import requests_cache

from bs4 import BeautifulSoup


class Site(object):
    headers = {"user-agent": "The Coolest Useragent"}

    def __init__(self, url, *args, **kwargs):
        self.html = requests.get(url, headers=self.headers).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        super().__init__(*args, **kwargs)

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
                    'title': link['title'],
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


def URLlist(filename):
    """
    List all URLs in urllist.csv

    .. todo::
        Sort and filter dupes.
    """
    from urllib.parse import urlparse
    with open(filename) as urls:
        urlreader = csv.reader(urls)
        for url in urlreader:
            yield urlparse(url[0]).geturl()


if __name__ == '__main__':
    websites = []
    requests_cache.install_cache('cache')

    for url in URLlist("urls.csv"):
        site = Site(url)
        try:
            siteDetail = {
                'url': str(url),
                'title': site.title,
                'feeds': site.feedSoup,
                'og': site.og,
            }
            websites.append({'site': siteDetail})
        except Exception as e:
            print("EXCEPTION: ", e)
            # print(e)
            # print(websites[-1])
            # print(type(websites[-1]))

    with open("sites.yaml", "w") as y:
        y.write(yaml.safe_dump(websites, default_flow_style=False))

    sys.exit(0)

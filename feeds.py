import csv
import yaml
from yaml import Dumper
import requests
import requests_cache

from bs4 import BeautifulSoup


def getSoup(site):
    html = requests.get(site)
    return BeautifulSoup(html.text, 'html.parser')


def getSiteMeta(soup):
    """returns 1st occurance of 'og:title', if any."""
    for m in soup("meta"):
        if 'og:title' in m.attrs:
            return m['og:title']
    """returns 1st occurance of itemprop 'name', if any."""
    for m in soup("meta"):
        if 'itemprop' in m.attrs:
            if m['itemprop'] == 'name':
                return m['content']
    if soup("title"):
        return soup.title.string


def URLlist(filename):
    with open(filename) as urls:
        urlreader = csv.reader(urls)
        for url in urlreader:
            yield url


if __name__ == '__main__':
    websites = []
    requests_cache.install_cache('cache')

    for url in URLlist("urls.csv"):
        try:
            title = getSiteMeta(getSoup(url[0]))
            websites.append({
                'url': str(url[0]),
                'title': str(title)
            })
        except Exception as e:
            print(e)

    with open("sites.yaml", "w") as y:
        y.write(yaml.safe_dump(websites, default_flow_style=False))

#!/usr/bin/env python

"""
Feed Details.

Get Feeds from Sites
"""

import feedparser
import pprint
from collections import Counter
import yaml
from datetime import datetime, timedelta
from time import mktime

from entries import processEntry, entryID

feedKeys = Counter(
    {
        'feed': 147,
        'entries': 147,
        'bozo': 147,
        'headers': 147,
        'href': 147,
        'status': 147,
        'encoding': 147,
        'version': 147,
        'namespaces': 147,
        'etag': 113,
        'updated': 113,
        'updated_parsed': 113,
        'bozo_exception': 6
    }
)


def FeedList(filename):
    """List of Feeds in `Feeds`.yaml"""
    with open(filename) as y:
        websites = yaml.load(y)
        for site in websites:
            if site.get('site', 'None'):
                for feed in site['site']['feeds']:
                    yield feed


def feedActive(updated, days=180):
    """Feed `u  pdated` had activity in the last `days`."""
    if updated is not None:
        period = datetime.now() - timedelta(days=days)
        return datetime(*updated[:6]) > period
    else:
        return True


if __name__ == '__main__':
    feed_keys = Counter()
    detail_keys = Counter()
    for feed in FeedList("sites.yaml"):
        f = feedparser.parse(feed['href'])
        if f.get('feed', None):
            feed_keys.update(f.keys())
            detail_keys.update(f.feed.keys())
            print(f.feed.get('title', None))
            updated = f.feed.get('updated_parsed', None)
            if feedActive(updated):
                print("Links: %s" % f.feed.get('links', None))
                print(f.feed.get('link', None))
                print(f.feed.get('title_detail', None))
                print(f.feed.get('subtitle', None))
                print(f.feed.get('subtitle_detail', None))
                print("Updated: %s", datetime(*updated[:6]))
                if f.entries:
                    print("Entries")
                    for entry in f.entries:
                        processEntry(entry)
            else:
                print("Older: %s" % datetime(*updated[:6]))

    print(feed_keys)
    print(detail_keys)

#!/usr/bin/env python

"""
entries.

Get Entries from Feeds
"""

import feedparser
import pprint
import yaml

from time import mktime
from datetime import datetime



# Counter({'title': 5490, 'title_detail': 5490, 'links': 5490, 'link': 5490, 'summary': 5487, 'id': 5390, 'published': 5340, 'published_parsed': 5340, 'guidislink': 5320, 'summary_detail': 5239, 'authors': 5018, 'author': 5018, 'author_detail': 5015, 'content': 4465, 'tags': 2742, 'comments': 2164, 'slash_comments': 2014, 'wfw_commentrss': 1984, 'itunes_duration': 484, 'subtitle': 484, 'subtitle_detail': 484, 'psc_chapters': 418, 'updated': 408, 'updated_parsed': 408, 'href': 288, 'media_thumbnail': 252, 'feedburner_origlink': 196, 'post-id': 184, 'gd_image': 181, 'media_content': 142, 'thr_total': 113, 'gd_extendedproperty': 75, 'media_credit': 67, 'credit': 67, 'source': 38, 'slash_department': 30, 'slash_section': 30, 'slash_hit_parade': 30, 'categories': 30, 'itunes_explicit': 20, 'itunes_block': 20, 'dc_abstract': 15, 'publisher': 15, 'publisher_detail': 15, 'itunes_episodetype': 10, 'link2picture': 10, 'link2picturemobile': 10, 'georss_featurename': 8, 'where': 8, 'twitter': 2, 'series_name': 2})


def timeStructToDatetime(t):
    if t is not None:
        return datetime.fromtimestamp(mktime(t))


def processEntry(entry):
    pubdate = timeStructToDatetime(entry.get('published_parsed', None))
    upddate = timeStructToDatetime(entry.get('updated_parsed', None))
    content = entry.get('content', None)

    def lastDate(pubdate, upddate):
        """Which happend last."""
        if not upddate and not pubdate:
            return datetime.now()
        if not upddate:
            return pubdate
        if upddate > pubdate:
            return upddate
        return pubdate

    recent = lastDate(pubdate, upddate)

    published = entry.get('published', None)
    updated = entry.get('updated', None)

    hl = "%s: %s - (%s)" % (
        pubdate,
        entry.get('id', 'No link'),
        entry.get('guidislink', 'id is no link')
    )
    print("ID: %s" % (entryID(entry)))
    print("Title: %s" % entry.get('title', 'No title'))
    print("Published: %s" % recent)
    print(hl)
    if content:
        print("Type: %s", type(content))
    print("-----")


def entryID(entry):
    """Try to make an unique ID for entry."""
    id = None
    if entry.get('guidislink', None):
        id = entry.get('id', None)
    if id is None:
        id = entry.get('link', None)
    if id is None:
        raise Exception
    return id


if __name__ == '__main__':
    from collections import Counter
    keys = Counter()
    with open("sites.yaml", "r") as y:
        websites = yaml.load(y)
        pp = pprint.PrettyPrinter(indent=4)
        for site in websites:
            print("\n\n\n")
            for feed in site['feeds']:
                f = feedparser.parse(feed['href'])
                if f.get('feed', None):
                    pp.pprint(f.feed.get('title', 'No Title'))
                    if f.entries:
                        for entry in f.entries:
                            keys.update(entry.keys())
    print(keys)

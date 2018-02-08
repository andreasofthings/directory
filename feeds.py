#!/usr/bin/env python

"""
Feed Details.

Get Feeds from Sites
"""

import feedparser
import pprint
from collections import Counter
import yaml

# Counter({'feed': 147, 'entries': 147, 'bozo': 147, 'headers': 147, 'href': 147, 'status': 147, 'encoding': 147, 'version': 147, 'namespaces': 147, 'etag': 113, 'updated': 113, 'updated_parsed': 113, 'bozo_exception': 6})

# Counter({'links': 147, 'title': 146, 'title_detail': 146, 'link': 146, 'subtitle': 145, 'subtitle_detail': 145, 'updated': 139, 'updated_parsed': 139, 'generator_detail': 108, 'generator': 108, 'sy_updateperiod': 98, 'sy_updatefrequency': 98, 'language': 90, 'image': 39, 'authors': 26, 'author': 26, 'author_detail': 24, 'tags': 21, 'feedburner_info': 17, 'site': 15, 'id': 13, 'guidislink': 13, 'published': 12, 'published_parsed': 12, 'publisher_detail': 11, 'opensearch_totalresults': 11, 'opensearch_startindex': 11, 'opensearch_itemsperpage': 11, 'summary': 10, 'summary_detail': 10, 'itunes_explicit': 10, 'rights': 9, 'rights_detail': 9, 'href': 9, 'gd_image': 9, 'itunes_block': 8, 'publisher': 5, 'docs': 5, 'rdf_li': 5, 'rdf_seq': 5, 'entries': 5, 'feedburner_emailserviceid': 5, 'feedburner_feedburnerhostname': 5, 'ttl': 4, 'feedburner_feedflare': 4, 'feedpress_locale': 2, 'fyyd_verify': 2, 'itunes_type': 2, 'sy_updatebase': 2, 'textinput': 2, 'cloud': 2, 'meta': 1, 'info': 1, 'info_detail': 1, 'xhtml_meta': 1, 'logo': 1})

def Feedlist(filename):
    with open(filename) as y:
        websites = yaml.load(y)
        for site in websites:
            for feed in site['feeds']:
                yield feed

if __name__ == '__main__':
    feed_keys = Counter()
    detail_keys = Counter()
    for feed in FeedList("sites.yaml"):
        f = feedparser.parse(feed['href'])
        if f.get('feed', None):
            feed_keys.update(f.keys())
            detail_keys.update(f.feed.keys())
    print(feed_keys)
    print(detail_keys)

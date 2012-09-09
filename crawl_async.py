from __future__ import with_statement

from eventlet.green import urllib2
import eventlet
import re
import redis
import json
from urlparse import urlparse
from bs4 import SoupStrainer, BeautifulSoup
import time

# base code taken from:
# http://eventlet.net/doc/examples.html#recursive-web-crawler

url_regex = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
domains_seen = set()
a_strainer = SoupStrainer('a')

def fetch(url, seen, pool, redisconn):
    """Fetch a url, stick any found urls into the seen set, and
    dispatch any new ones to the pool."""
    print "fetching", url
    html = ''
    with eventlet.Timeout(5, False):
        domains_seen.add(urlparse(url).hostname)
        html = urllib2.urlopen(url).read().lower()

    wordcount = {}
    for word in splitter.split(BeautifulSoup(html).text):
        wordcount[word] = wordcount.get(word, 0.0) + 1
    
    redisconn.publish('wordcount', json.dumps(wordcount))

    for a in BeautifulSoup(html, "html.parser", parse_only=a_strainer):
        if "href" in a.attrs and a['href'].startswith('http'):
            new_url = a['href']
            domain = urlparse(new_url).hostname
            # only send requests to new domains
            if new_url not in seen and domain not in domains_seen:
                seen.add(new_url)
                # while this seems stack-recursive, it's actually not:
                # spawned greenthreads start their own stacks
                pool.spawn_n(fetch, new_url, seen, pool, redisconn)

            
def crawl(start_url):
    """Recursively crawl starting from *start_url*.  Returns a set of 
    urls that were found."""
    pool = eventlet.GreenPool(3)
    r = redis.StrictRedis()
    seen = set()
    fetch(start_url, seen, pool, r)
    pool.waitall()
    return seen

splitter = re.compile("\\W+")
seen = crawl("http://cnn.com")

print "I saw these urls:"
print "\n".join(seen)
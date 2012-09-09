import redis
import json
import urllib2, urlparse
from bs4 import SoupStrainer, BeautifulSoup
import re
import random


def get_http(url):
    try:
        src = urllib2.urlopen(url).read()
    except:
        src = ""
    return src

def get_urls(url, html):

    # host = urlparse.urlparse(url).hostname
    # domains.get(host)

    wordcount = {}
    print "Getting word count for %s" % url
    for word in splitter.split(html):
        wordcount[word] = wordcount.get(word, 0) + 1
    
    r.publish('wordcount', json.dumps(wordcount))

    for a in BeautifulSoup(html, "html.parser", parse_only=a_strainer):
        if "href" in a.attrs and a['href'].startswith('http'):
            seen.add(url)
            if a['href'] in seen: return

            get_urls(a['href'], get_http(a['href']))


domains = {}
seen = set()

a_strainer = SoupStrainer('a')
splitter = re.compile("\\W+")

r = redis.StrictRedis()

def main():
    url = "http://www.cnn.com/"
    get_urls(url, get_http(url))

if __name__ == '__main__':
    main()






    







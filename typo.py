from __future__ import absolute_import

__all__ = ['app']

from urlparse import urlparse, urlunparse
from flask import Flask, request, redirect
from tldextract import extract
from fuzzywuzzy import process

BASE = 'sabf.org.ar'
CUTOFF = 80
DEFAULT_SITE = 'www'
MATCH_SITES = {
    'site': 'www',
    'blog': 'blog',
    'apply': 'apply',
    'recruiting': 'www',
}

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route(r'/<path:path>')
def catch_all(path):
    redirect_to = get_best_match(request.url)
    new_url = replace_host(request.url, redirect_to)
    return redirect(new_url)

def replace_host(url, host):
    parsed = urlparse(url)
    netloc = u'%s.%s' % (host, BASE)
    parsed = parsed[:1] + (netloc,) + parsed[2:]
    return urlunparse(parsed)

def get_best_match(url):
    original_url = extract(request.url)
    sub = original_url.subdomain
    closest = process.extractOne(sub, MATCH_SITES.keys(),
            score_cutoff=CUTOFF)
    return MATCH_SITES.get(closest, DEFAULT_SITE)

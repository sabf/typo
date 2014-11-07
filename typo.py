from __future__ import absolute_import

__all__ = ['app']

from ConfigParser import SafeConfigParser as ConfigParser
from urlparse import urlparse, urlunparse

from flask import Flask, request, redirect
from fuzzywuzzy import process
from tldextract import extract

config = ConfigParser()
config.read(['config.ini', 'config.ini.tpl'])

BASE = config.get('typo', 'base')
CUTOFF = config.getint('typo', 'cutoff')
DEFAULT_SITE = config.get('typo', 'default_site')
MATCH_SITES = dict(config.items('match_sites'))

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
    return urlunparse(parsed[:1] + (netloc,) + parsed[2:])

def get_best_match(url):
    original_url = extract(request.url)
    sub = original_url.subdomain
    closest = process.extractOne(sub, MATCH_SITES.keys(),
            score_cutoff=CUTOFF)
    return MATCH_SITES.get(closest, DEFAULT_SITE)

from __future__ import with_statement

import os

from fabric.api import *
from fabric.contrib.files import upload_template


BASE = "/srv"
REPO = "git@github.com:sabf/typo.git"

# env injector. See:
# https://github.com/jacobian/django-dotenv/blob/master/dotenv.py


def _load_env():
    dotenv = os.path.join(os.path.dirname(__file__), '.env')
    for line in open(dotenv):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        v = v.strip("'").strip('"')
        os.environ.setdefault(k, v)

try:
    _load_env()
except IOError:
    print "Can't load .env file."

default_target = os.path.dirname(os.path.realpath(__file__))
TARGET = os.environ.get("FAB_DEPLOY_TARGET", default_target)


## Fab commands

def flask_deploy(rev=None, user="www-data", reset=False):
    run("rm uwsgi.ini", user=user)
    if reset:
        run("git reset --hard", user=user)
    run("git pull", user=user)
    branch = 'master' if not rev else rev
    if branch:
        run("git checkout {branch}".format(branch=rev))
    run("git pull origin {branch}".format(branch=rev))
    with prefix(". env/bin/activate"):
        run("pip install -r requirements.txt", user=user)
    run("ln -s uwsgi.app uwsgi.ini", user=user)

def restart_service(target):
    sudo("service {target} restart".format(target=target))

def update(branch=None, target=None, user='www-data'):
    path = os.path.join(BASE, target or TARGET)
    with cd(path):
        flask_deploy(branch, user)
        # let's play it safe...
        # restart_service("uwsgi")
        # restart_service("nginx")

def setup_venv(user, target=None):
    directory = os.path.join(BASE, target or TARGET)
    with cd(directory):
        sudo("virtualenv {target}/env/".format(target=target))
        sudo("chown -R {user}:{user} {target}".format(**locals()))

def setup(branch='master', user='www-data', target=None):
    target = target or TARGET
    directory = os.path.join(BASE, target)
    with cd(directory):
        sudo("apt-get install -y python-distribute python-virtualenv")
        # pull from git repo
        destroy(target=target)
        sudo("git clone {url} {target}".format(url=REPO, target=target))
        setup_venv(user, target)
        update(branch, target, user)

def destroy(target=None):
    target = target or TARGET
    directory = os.path.join(BASE, target)
    with cd(directory):
        sudo("rm -rf {dst}".format(dst=target))

def deploy(branch="master", target=None):
    update(branch, target)

def devel(branch="development", target=None):
    deploy(branch, target)

def run(port=8080):
    with prefix(". env/bin/activate"):
        local("python runserver.py 0.0.0.0:%s" % (port,))

def prepare():
    local("virtualenv env")
    with prefix(". env/bin/activate"):
        local("pip install -r requirements.txt")

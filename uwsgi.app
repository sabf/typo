[uwsgi]
module = typo:app
pythonpath = %d
virtualenv = %denv
chdir = %d

touch-reload = %d/uwsgi.ini
touch-reload = %d/uwsgi.app
touch-reload = %d/typo.py

harakiri = 10
max-requests = 500
vacuum = true
process = 1

add-header = X-Typo: True

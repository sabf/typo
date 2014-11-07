[uwsgi]
module = typo:app
pythonpath = %d
env = %denv

touch-reload = %d/uwsgi.ini
touch-reload = %d/uwsgi.app
touch-reload = %d/typo.py

harakiri = 10
max-requests = 500
vacuum = truevacuum = true
process = 1


#!/usr/bin/env sh
set -e

# make the changes on DB
python3 manage.py makemigrations
python3 manage.py migrate

# copy static files to static dir
python3 manage.py collectstatic --noinput

# start django server
python3 manage.py runserver 0.0.0.0:8000

# run gunicorn
# CMD ["gunicorn", "config.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]
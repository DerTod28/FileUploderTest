#!/bin/bash

set -e

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py createadmin
gunicorn picasso.wsgi:application -w 6 -b :8010

#!/bin/sh

python ./manage.py migrate

gunicorn healthbuddy_backend.wsgi -c gunicorn/gunicorn.conf.py

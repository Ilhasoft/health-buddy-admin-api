#!/bin/sh

celery -A healthbuddy_backend.celery worker --loglevel=info

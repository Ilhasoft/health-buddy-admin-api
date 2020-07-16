#!/bin/sh

celery -A healthbuddy_backend.celery beat --loglevel=info

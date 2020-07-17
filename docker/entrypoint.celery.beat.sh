#!/bin/sh

celery --pidfile= -A healthbuddy_backend.celery beat --loglevel=info

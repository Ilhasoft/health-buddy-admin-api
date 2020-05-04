import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = workers

bind = "0.0.0.0:8000"
env = "DJANGO_SETTINGS_MODULE=healthbuddy_backend.settings"
loglevel = "debug"
accesslog = "gunicorn.access"
errorlog = "gunicorn.error"
chdir = "/app"
capture_output = True

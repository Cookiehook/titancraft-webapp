import multiprocessing

bind = "unix:/app/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "project.wsgi:application"

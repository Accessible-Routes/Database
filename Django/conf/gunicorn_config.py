import os
import environ

env = environ.Env()
environ.Env.read_env()

command = '/home/ubuntu/django_env/bin/gunicorn'
pythonpath = '/home/ubuntu/Database/Django/backend/'
bind = env("IP_PORT")
workers = 3
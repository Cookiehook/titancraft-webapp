import re

import requests

from project.settings import *  # noqa. Wildcard import is used to mimic inheritance

DEBUG = False
SECRET_KEY = get_secret('TITANCRAFT_WEBAPP_SECRET_KEY')
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "titancraft.cookiehook.com"]
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

try:  # Add the EC2's own IP address, used by the ALB health checker
    ALLOWED_HOSTS.append(requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=1).text)
except requests.exceptions.RequestException:
    pass

dsn = get_secret("titancraft_db_dsn")
opts = re.findall("postgresql://(.+):(.+)@(.+):(.+)", dsn)[0]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': opts[0],
        'PASSWORD': opts[1],
        'HOST': opts[2],
        'PORT':  opts[3]
    }
}

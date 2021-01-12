# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 18:27:55 2021

@author: Mayuko
"""

from .base import *
import dj_database_url
from socket import gethostname

hostname = gethostname()

db_from_env = dj_database_url.config()

DATABASES = {
    'default': dj_database_url.config()
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

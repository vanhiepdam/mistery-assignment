# -*- coding: utf-8 -*-
import dj_database_url

from .base import *

CORS_ALLOWED_ORIGINS = [
    'https://mistery-assignment.herokuapp.com'
]

DATABASES = {
    'default': dj_database_url.config(env='HEROKU_POSTGRESQL_GREEN_URL')
}

import os
import urlparse


class Config(object):
    '''Default configuration object.'''

    DEBUG = False
    TESTING = False
    PORT = int(os.environ.get('PORT', 5000))


class ProductionConfig(Config):
    '''Configuration object specific to production environments.'''

    REDIS_URL = os.environ.get('REDISTOGO_URL')
    if REDIS_URL:
        url = urlparse.urlparse(REDIS_URL)
        REDIS_HOST = url.hostname
        REDIS_PORT = url.port
        REDIS_PASSWORD = url.password

    MONGOLAB_URI = os.environ.get('MONGOLAB_URI')
    if MONGOLAB_URI:
        url = urlparse.urlparse(MONGOLAB_URI)
        MONGODB_USER = url.username
        MONGODB_PASSWORD = url.password
        MONGODB_HOST = url.hostname
        MONGODB_PORT = url.port
        MONGODB_DB = url.path[1:]


class DevelopmentConfig(Config):
    '''Configuration object specific to development environments.'''

    DEBUG = True

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DB = os.environ.get('DBNAME', 'taarifa_backend')

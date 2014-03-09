import urlparse
import logging

from os import environ
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore


# configure the logging
logging.basicConfig(level='DEBUG',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
if environ.get('MONGOLAB_URI'):
    url = urlparse.urlparse(environ['MONGOLAB_URI'])
    app.config['MONGODB_SETTINGS'] = {'username': url.username,
                                      'password': url.password,
                                      'host': url.hostname,
                                      'port': url.port,
                                      'db': url.path[1:]}
else:
    app.config['MONGODB_SETTINGS'] = {'db': environ.get("DBNAME", "taarifa_backend")}
app.config['SECRET_KEY'] = 'hush'

db = MongoEngine(app)

import models
#TODO: where is this currently used? --nweinert
user_datastore = MongoEngineUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

from taarifa_backend.api import api
app.register_blueprint(api)

if __name__ == '__main__':
    app.run()

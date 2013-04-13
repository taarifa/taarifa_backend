from flask import Flask
from flask.ext.mongoengine import MongoEngine
import logging
# configure the logging
logging.basicConfig(level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "taarifa_backend"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

def register_views():
    """
    to avoid circular dependencies and register the routes
    """
    from api import receive_report
    pass

register_views()
app.logger.debug('Registered views are: \n' + app.view_functions.keys().__repr__())

if __name__ == '__main__':
    app.run()

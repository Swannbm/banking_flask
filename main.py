import logging
import logging.config
from model import session as db
from flask import Flask # pip install flask
from flask_debugtoolbar import DebugToolbarExtension # pip install flask_debugtoolbar

# maitre JeuDridi modif

logging.config.fileConfig('bankin_flask/log.ini')
log = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = False # switch to True when developing
app.config['SECRET_KEY'] = "Gustave Eiffel a construit une merveille tout d'acier et de rivets"
toolbar = DebugToolbarExtension(app)

@app.teardown_appcontext
def cleanup(resp_or_exc):
    """ usefull to make sqlalchemy working with flask """
    db.remove()

import controler

if __name__ == '__main__':
    app.add_url_rule('/', 'home', view_func=controler.home)
    app.add_url_rule('/client/add', 'add_client', view_func=controler.add_client, methods=['POST', 'GET'])
    app.add_url_rule(
            '/client/file/<int:client_id>',
            'client_file',
            view_func=controler.client_file,
            methods=['POST', 'GET'])
    app.add_url_rule(
            '/client/account/add/<int:client_id>/<int:type>',
            'add_account',
            view_func=controler.add_account)
    try:
        log.info('Application starting')
        app.run(host='127.0.0.1', port=8080)
        log.info('Application end without exception')
    except Exception as toto:
        log.exception('Application end because of uncatching exception')

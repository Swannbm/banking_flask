import logging
import logging.config
from model import session as db
from flask import Flask # pip install flask
from flask_debugtoolbar import DebugToolbarExtension # pip install flask_debugtoolbar


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

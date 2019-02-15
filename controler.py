import logging
import view
from model import Client, SavingAccount, DebitAccount, BankAccount
from model import session as db
from flask import render_template, request, redirect, url_for


log = logging.getLogger(__name__)


def home():
    log.info('Controler home starts')
    clients = db.query(Client).order_by(Client.lastname)
    return render_template('home.html', clients=clients)


def add_client():
    log.info('Controler add_clients starts')
    if request.method == 'POST':
        # TODO check that firstname and lastname are defined
        client = Client(
                request.form['firstname'],
                request.form['lastname'],
                request.form['email'])
        db.add(client)
        db.commit()
        return redirect(url_for('client_file', client_id=client.client_id))
    else:
        return render_template('add_client.html')


def get_amount():
    """ Ensure that request.form['amount'] is a strictly positive float and return its value """
    try:
        amount = float(request.form['amount'])
    except ValueError as ve:
        raise ValueError('Please, enter only digits in amount.')
    if amount == 0:
        raise ValueError('Amount must not be zero (0).')
    elif amount < 0:
        raise ValueError('Amount must be positive.')
    else:
        return amount


def client_file(client_id):
    log.info('Controler client_file starts')
    client = db.query(Client).get(client_id)
    if request.method == 'POST':
        account_number = request.form['account_number']
        account = db.query(BankAccount).get(account_number)
        if request.form['action'] == 'interest':
            earned = account.interest()
            account.credit(earned)
        else:
            try:
                amount = get_amount()
            except ValueError as e:
                return render_template('client_file.html', client=client, error=e)
            # user wants to credit or debit an account
            if request.form['action'] == 'credit':
                account.credit(amount)
            else:
                account.debit(amount)
        db.commit()
    return render_template('client_file.html', client=client)


def add_account(client_id, type):
    log.info('Controler add_account starts')
    if type == 1:
        account = DebitAccount(client_id)
    else:
        account = SavingAccount(client_id, 0.03)
    db.add(account)
    db.commit()
    return redirect(url_for('client_file', client_id=client_id))


def display_account(account):
    log.info('Controler display_account starts')
    raise NotImplementedError()

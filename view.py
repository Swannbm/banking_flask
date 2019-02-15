from os import system

def input_advanced(quest):
    resp = None
    while resp == None:
        resp = input(quest)
        try:
            return int(resp)
        except ValueError as ve:
            resp = None
            print('Error message : value not correct, retry.')

def home():
    system('cls')
    print('   HOME MENU')
    print()
    print('1 - Clients list')
    print('2 - Add client')
    print()
    print('0 - Exit')
    print()
    return input_advanced('Choice=')

def add_client():
    system('cls')
    print('   ADD CLIENT')
    print()
    fn = input('Firstname=')
    ln = input('Lastname=')
    em = input('Email=')
    return fn, ln, em

def display_client_file(client):
    system('cls')
    print('   CLIENT FILE')
    print()
    print('{} {}'.format(client.firstname, client.lastname))
    print()
    print('Accounts:')
    for i, account in enumerate(client.accounts):
        print('', i+1, '-', account)
    print()
    print('-1 - Add account')
    print(' 0 - exit')
    return int(input('choice='))

def display_add_account():
    system('cls')
    print('   ADD ACCOUNT')
    print()
    print('Choose type of account to add :')
    print('1 - Debit account')
    print('2 - Saving account')
    print()
    return int(input('Choice='))
    
def display_client_list(clients):
    system('cls')
    print('   CLIENTS LIST')
    print()
    for i, client in enumerate(clients):
        print('{0:>3} - {1} {2}'.format(i+1, client.firstname, client.lastname))
    print()
    print('  0 - Exit')
    print()
    return int(input('Choice='))

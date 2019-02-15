from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session


engine = create_engine('sqlite:///bankin.db', echo=False)
Base = declarative_base(bind=engine)
session = scoped_session(sessionmaker(bind=engine))


class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email = Column(String(75), nullable=True)
    accounts = relationship("BankAccount", back_populates="client")

    def __init__(self, firstname, lastname, email):
        self.firstname = firstname.capitalize()
        self.lastname = lastname.upper()
        self.email = email.lower()
        self.accounts = []

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    number = Column(Integer, primary_key=True)
    _balance = Column(Float)
    client_id = Column(ForeignKey('clients.client_id'))
    client = relationship("Client", back_populates="accounts")
    type = Column(String(20))
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'bank_account'
    }

    def __init__(self, client_id):
        self.client_id = client_id
        self._balance = 0

    def credit(self, amount):
        if amount >= 0:
            self._balance += amount
        else:
            raise Exception("You can't add a negative value to the account balance")

    def get_account_balance(self):
        return self._balance

    @property
    def get_type_name(self):
        return 'General acount'

    def __str__(self):
        return 'General account ({})'.format(self.number)


class DebitAccount(BankAccount):
    __mapper_args__ = {
        'polymorphic_identity': 'debit_accounts'
    }

    def debit(self, amount):
        if amount >= 0:
            self._balance -= amount
        else:
            raise Exception("You can't soustract a negative value to the account balance")
    
    @property
    def get_type_name(self):
        return 'Debit acount'

    def __str__(self):
        return 'Debit {} {}'.format(self.number, self._balance)


class SavingAccount(BankAccount):
    __mapper_args__ = {
        'polymorphic_identity': 'saving_accounts'
    }
    rate = Column(Float)

    def __init__(self, client_id, rate):
        super().__init__(client_id)
        self.rate = rate

    def interest(self):
        return self._balance * self.rate

    @property
    def get_type_name(self):
        return 'Saving acount'

    def __str__(self):
        return 'Saving {} {}'.format(self.number, self._balance)

Base.metadata.create_all(engine)

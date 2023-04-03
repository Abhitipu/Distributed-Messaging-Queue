import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'Account'
    account_id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
    
    def __repr__(self) -> str:
        return f'Account {self.account_id}: {self.balance}'

    @staticmethod
    def ListAccounts():
        return Account.query.all()

    @staticmethod
    def CheckBalance(account_id):
        if Account.CheckAccountExists(account_id) is False:
            return -1
        return Account.query.filter_by(account_id=account_id).first().balance

    @staticmethod
    def CheckAccountExists(account_id):
        return Account.query.filter_by(account_id=account_id).first() is not None

    @staticmethod
    def CreateAccount():
        account_id = uuid.uuid4().int
        account = Account(account_id, 0)
        db.session.add(account)
        db.session.commit()
        return account_id
    
    @staticmethod
    def Deposit(account_id, amount):
        if Account.CheckAccountExists(account_id) is False:
            return -1
        
        account = Account.query.filter_by(account_id=account_id).first()
        account.balance += amount
        db.session.commit()
        return 1
    
    @staticmethod
    def Withdraw(account_id, amount):
        if Account.CheckAccountExists(account_id) is False:
            return -1
        
        account = Account.query.filter_by(account_id=account_id).first()
        if account.balance - amount < 0:
            return -2
        account.balance -= amount
        db.session.commit()
        return 1

    @staticmethod
    def Transfer(from_account_id, to_account_id, amount):
        if Account.CheckAccountExists(from_account_id) is False or Account.CheckAccountExists(to_account_id) is False:
            return -1
        
        if Account.Withdraw(from_account_id, amount) is False:
            return -2
        
        Account.Deposit(to_account_id, amount)
        return 1
    
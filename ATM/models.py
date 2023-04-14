import uuid
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from pysyncobj import SyncObj, replicated, replicated_sync, SyncObjConf

from create_app import get_app


class ReplicatedAccount(SyncObj):
    def __init__(self, self_addr=None, addr_list=None):
        self_addr = os.getenv('HOSTNAME')+':'+os.getenv('PORT')
        base_broker = '_'.join(os.getenv('HOSTNAME').split('_')[:-1])
        addr_list = []
        for suffix in ['one', 'two', 'three', 'four']:
            if suffix != os.getenv('HOSTNAME').split('_')[-1]:
                addr_list.append(base_broker + '_' + suffix +
                                 ':' + os.getenv('PORT'))
        print(f"self_addr: {self_addr}")
        print(f"addr_list: {addr_list}")
        super(ReplicatedAccount, self).__init__(self_addr, addr_list)

    @replicated
    def _create(self,account_id):
        return Account.CreateAccount(account_id)

    def create(self):
        account_id = uuid.uuid4()
        return self._create(account_id,sync=False)

    @replicated
    def deposit(self, account_id, amount):
        return Account.Deposit(account_id, amount)
    
    @replicated
    def withdraw(self, account_id, amount):
        return Account.Withdraw(account_id, amount)

    @replicated
    def transfer(self, from_account_id, to_account_id, amount):
        return Account.Transfer(from_account_id, to_account_id, amount)

class Account(db.Model):
    __tablename__ = 'Account'
    account_id = db.Column(db.String, primary_key=True)
    balance = db.Column(db.Integer)
    app = get_app()

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
    
    def __repr__(self) -> str:
        return f'Account {self.account_id}: {self.balance}'

    @staticmethod
    def ListAccounts():
        with get_app().app_context():
            return Account.query.all()

    @staticmethod
    def CheckBalance(account_id):
        with get_app().app_context():
            if Account.CheckAccountExists(account_id) is False:
                return -1
            return Account.query.filter_by(account_id=account_id).first().balance

    @staticmethod
    def CheckAccountExists(account_id):
        with get_app().app_context():
            return Account.query.filter_by(account_id=account_id).first() is not None

    @staticmethod
    def CreateAccount(account_id):
        with get_app().app_context():
            account = Account(account_id, 0)
            db.session.add(account)
            db.session.commit()
            return account_id
        
    @staticmethod
    def Deposit(account_id, amount):
        with get_app().app_context():
            print("Deposit")
            if Account.CheckAccountExists(account_id) is False:
                return -1
            
            account = Account.query.filter_by(account_id=account_id).first()
            account.balance += int(amount)
            db.session.commit()
            return 1
    
    @staticmethod
    def Withdraw(account_id, amount):
        with get_app().app_context():
            amount = int(amount)
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
        with get_app().app_context():
            amount = int(amount)
            if Account.CheckAccountExists(from_account_id) is False or Account.CheckAccountExists(to_account_id) is False:
                return -1
            
            if Account.Withdraw(from_account_id, amount) < 0:
                return -2
            Account.Deposit(to_account_id, amount)
            return 1
    
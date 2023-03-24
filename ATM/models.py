# from sqlalchemy import Column, Integer
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import declarative_base

# Base = declarative_base()

from app import db
from datetime import datetime

# class Account(Base):
#     """The Account class corresponds to the "accounts" database table.
#     """
#     __tablename__ = 'accounts'
#     id = Column(UUID(as_uuid=True), primary_key=True)
#     balance = Column(Integer)

class Transactions(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer(), db.ForeignKey('Account.account_id'))
    receiver_id = db.Column(db.Integer(), db.ForeignKey('Account.account_id'))
    amount = db.Column(db.Integer)

    def __init__(self, sender_id, receiver_id, amount):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount

class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
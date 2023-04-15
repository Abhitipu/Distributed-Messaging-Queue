from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
# from cockroachdb.sqlalchemy import run_transaction

import os
from models import Account, db, ReplicatedAccount

from create_app import get_app

app = get_app()

DATABASE_CONFIG = {
    'driver': 'postgresql',
    'host': os.getenv('DB_NAME'),
    'user': 'postgres',
    'port': 5432,
    'dbname': os.getenv('DB_NAME'),
    'password' : 'postgres'
}

db_uri = f"{DATABASE_CONFIG['driver']}://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['SECRET_KEY'] = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    # 'application_name': f'$ atm_flask_{os.getenv("HOST_NAME")}'}

app.config['DEBUG'] = True
db.init_app(app)

_replicated_account: ReplicatedAccount = None

def create_sync_obj():
    global _replicated_account
    if _replicated_account:
        return

    _replicated_account = ReplicatedAccount()
    _replicated_account.waitBinded()
    _replicated_account.waitReady()

    print('Sync object is created')


def replicated_account():
    global _replicated_account
    if _replicated_account:
        return _replicated_account

    raise Exception('Sync object is not created')

@app.route('/', methods=['GET'])
def home():
    dict = request.get_json()
    account_id = dict['account_id']
    print(account_id)
    if Account.CheckAccountExists(account_id) is False:
        return {
            "status": "Failure",
        }
    else:
        return {
            "status": "Success",
        }

# @app.route('/showall', methods=['GET'])
# def show_all():
#     all_accounts = Account.ListAccounts()
#     response = {
#         "status": "Success",
#         "accounts": all_accounts 
#     }
#     return response

@app.route('/create', methods=['POST'])
def create():
    account_id = replicated_account().create()
    response = {
        "status": "Success",
        "account_id": account_id
    }
    return response


@app.route('/withdraw', methods=['POST'])
def withdraw():
    dict = request.get_json()
    status = replicated_account().withdraw(dict['account_id'], dict['amount'],sync=True)
    
    if status == -1:
        response = {
            "status": "Failure",
            "message": "Incorrect account id"
        }
    elif status == -2:
        response = {
            "status": "Failure",
            "message": "Insufficient balance"
        }
    else:
        response = {
            "status": "Success",
            "message": "Withdraw successful"
        }
    
    return response

@app.route('/deposit', methods=['POST'])
def deposit():
    dict = request.get_json()
    status = replicated_account().deposit(dict['account_id'], dict['amount'],sync=True)
    
    if status == -1:
        response = {
            "status": "Failure",
            "message": "Incorrect account id"
        }
    else:
        response = {
            "status": "Success",
            "message": "Deposit successful"
        }
        
    return response


@app.route('/balance', methods=['GET'])
def get_balance():
    dict = request.get_json()
    balance = Account.CheckBalance(dict['account_id'])
    
    if balance == -1:
        response = {
            "status": "Failure",
            "message": "Incorrect account id"
        }
    else:
        response = {
            "status": "Success",
            "balance": balance
        }
        
    return response


@app.route('/transfer', methods=['POST'])
def transfer():
    dict = request.get_json()
    status = replicated_account().transfer(dict['from_account_id'], dict['to_account_id'], dict['amount'],sync=True)
    if status == -1:
        response = {
            "status": "Failure",
            "message": "Incorrect account id"
        }
    elif status == -2:
        response = {
            "status": "Failure",
            "message": "Insufficient balance"
        }
    else:
        response = {
            "status": "Success",
            "message": "Transfer successful"
        }
    
    return response


import threading
import time

def singleTickFunc(o, timeToTick, interval, stopFunc):
    currTime = time.time()
    finishTime = currTime + timeToTick
    while time.time() < finishTime:
        o._onTick(interval)
        if stopFunc is not None:
            if stopFunc():
                break
            
def doTicks(objects, timeToTick, interval=0.05, stopFunc=None):
    threads = []
    for o in objects:
        t = threading.Thread(target=singleTickFunc, args=(o, timeToTick, interval, stopFunc))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
        
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all() # <--- create db object.
        create_sync_obj()

	
    # print(replicated_account()._isReady())
    # # print(replicated_account2._isReady())
    # # print(replicated_account3._isReady())
    
    # objs = [replicated_account]
    
    # doTicks(objs, 10.0, stopFunc=lambda: replicated_account._isReady() )
    # replicated_account.waitBinded()
    # replicated_account._printStatus()
    
    # print(replicated_account._isReady())
    
    # # print(replicated_account2._isReady())
    # # print(replicated_account3._isReady())
    
    # print(replicated_account._getLeader())
    # print(replicated_account2._getLeader())
    # print(replicated_account3._getLeader())
    
    app.run(host='0.0.0.0',port = 8081,threaded=True,debug=False)

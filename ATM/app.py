from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
# from cockroachdb.sqlalchemy import run_transaction

import os
from models import Account, db


app = Flask(__name__)
DATABASE_CONFIG = {
    'driver': 'postgresql',
    'host': os.getenv('HOST_NAME'),
    'user': 'postgres',
    'port': 5432,
    'dbname': os.getenv('DB_NAME'),
}

db_uri = f"{DATABASE_CONFIG['driver']}://{DATABASE_CONFIG['user']}:postgres@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['SECRET_KEY'] = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    # 'application_name': f'$ atm_flask_{os.getenv("HOST_NAME")}'}

app.config['DEBUG'] = True
db.init_app(app)

# sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

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
    account_id = Account.CreateAccount()
    response = {
        "status": "Success",
        "account_id": account_id
    }
    return response


@app.route('/withdraw', methods=['POST'])
def withdraw():
    dict = request.get_json()
    status = Account.Withdraw(dict['account_id'], dict['amount'])
    
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
    status = Account.Deposit(dict['account_id'], dict['amount'])
    
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
    status = Account.Transfer(dict['from_account_id'], dict['to_account_id'], dict['amount'])
    
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # <--- create db object.
	
    app.run(host='0.0.0.0')

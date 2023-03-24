from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction
from models import Transactions, Account

import os

app = Flask(__name__)
DATABASE_CONFIG = {
    'driver': 'cockroachdb',
    'host': os.getenv('HOST_NAME'),
    'user': 'root',
    'port': 26257,
    'dbname': os.getenv('DB_NAME'),
}
db_uri = f"{DATABASE_CONFIG['driver']}://{DATABASE_CONFIG['user']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}?sslmode=disable"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['SECRET_KEY'] = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'application_name': f'$ atm_flask_{os.getenv("HOST_NAME")}'}
app.config['DEBUG'] = True
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()


@app.route('/')
def show_all():
    def callback(session):
        return render_template(
            'show_all.html',
            todos=session.query(Todo).order_by(Todo.pub_date.desc()).all())
    return run_transaction(sessionmaker, callback)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            def callback(session):
                todo = Todo(request.form['title'], request.form['text'])
                session.add(todo)
            run_transaction(sessionmaker, callback)
            flash(u'Todo item was successfully created')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/update', methods=['POST'])
def update_done():
    if not request.form['account_id']:
        flash('Account ID is required', 'error')
    if not request.form['amount']:
        flash('Amount is required', 'error')

    def callback(session):
        session.query(Account).filter_by(account_id=request.form['account_id'])    
        pass
    
    return run_transaction(sessionmaker, callback)
    # flash('Updated status')
    # return redirect(url_for('show_all'))


@app.route('/withdraw', methods=['POST'])
def withdraw():
    def callback(session):
        # for account in session.query(Account)
        pass

    txn_details = run_transaction(sessionmaker, callback)
    # flash('Withdrawn money')
    return txn_details


@app.route('/deposit', methods=['POST'])
def deposit():
    pass


@app.route('/balance', methods=['GET'])
def get_balance():
    pass


@app.route('/transfer', methods=['POST'])
def transfer():
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # <--- create db object.
	
    app.run(host='0.0.0.0')

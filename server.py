import sys, os

sys.path.append(os.getcwd())

from flask import Flask, render_template, redirect, session, request, flash, url_for
from models.fact_model import FactModel
from models.base_model import DBSingelton
from models.user import User


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


@app.before_first_request
def initialize_tables() :
    connect_db()
    if not FactModel.table_exists() :
        FactModel.create_table()

    if not User.table_exists() :
        User.create_table()

    disconnect_db()


@app.before_request
def connect_db() :
    DBSingelton.getInstance().connect()


@app.teardown_request
def disconnect_db(err = None) :
    DBSingelton.getInstance().close()


# @app.route("/table/<int:column>/<int:row>")
# 	def show_table(row,column):
# 		return render_template("table.html", row=row, column = column)

# @app.route("/table/<int:column>/<int:row>")
# 	def show_table(row,column):
#         table = []
#         for row_index in range(1, row + 1):
#             row = []
#             for column_index in range(1, column + 1):
#                 row.append(row_index*column_index)
#             table.append(row)
#     return render_template("table.html", thebesttable=table)

@app.route('/')
def home():
    context = dict(title='Welcome to our website')
    return render_template('index.html', **context)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    context = dict(title='Create an account')

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')

        new_user = User(email=email, username=username, name=name, password=password)
        new_user.save()

    return render_template('signup.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    context = dict(title='Login')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = User\
                    .select().where(User.email == email)\
                    .where(User.password == password)\
                    .get()

            flash('Welcome back, {} {}'.format(user.first_name, user.last_name), category='info')
         
            session['user'] = {
                'name': '{} {}'.format(user.first_name, user.last_name),
                'email': user.email
            }

            return redirect(url_for('welcome'))
        except Exception as exception:
            flash('Sorry, you entered wrong credentials. Error: {}'.format(exception), category='danger')

    return render_template('login.html', **context)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/facts')
def facts():
    pass

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have successfully logged out', category='info')
    return redirect(url_for('home'))
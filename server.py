import sys, os

sys.path.append(os.getcwd())

from flask import Flask, render_template, redirect, session, request, flash
from models.fact_model import FactModel
from models.base_model import DBSingelton
from models.user import User


app = Flask(__name__)


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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')


        new_user = User(User.email = email, User.username == username, User.name == name
                          User.password == password )
        new_user.save()



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = User.select().where(User.email == email).where(User.password == password)
        except UserDoesNotExist, e:
            return 'User does not exist'
        return '{}'.format(user.get())

        if not user:
            pass
        else:
            flash('Sorry, you entered wrong credentials', category='error')
    return render_template('login.html')


@app.route('/welcome')
def welcome(username):
    if username == User.username:
        welcome_user = User.select(User.username)

    return render_template('welcome.html', name=User.username)


app.secret_key = os.environ.get("FLASK_SECRET_KEY")

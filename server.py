from flask import Flask,render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField,validators
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'SecretTestKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
migrate = Migrate(app, db) 

class Usuario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.Text)
    email = db.Column(db.Text)
    senha = db.Column(db.Text)

    def __init__(self,nome,email,senha):
        self.nome = nome
        self.email = email
        self.senha = senha
    def __repr__(self):
        return f"Usuário {self.nome} - Email {self.email}"


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField('Senha', validators=[validators.DataRequired()])
    submit = SubmitField('Login')



@app.route("/")
def index():
    content = {}
    return render_template('index.html')



@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    print("Entrou1")
    if form.validate_on_submit():
        flash("Logado com Sucesso!", 'success')
        session['usuario'] = form.email.data
        print('Entrou')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route("/list")
def listusers():
    content = {}
    return render_template('list.html')

@app.route("/new")
def adduser():
    content = {}
    return render_template('adduser.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404





if __name__ == '__main__':
    app.run(debug=True)
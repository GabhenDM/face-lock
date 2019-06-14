from flask import Flask,render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField,validators
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin,logout_user
import bcrypt


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'SecretTestKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db) 

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class Usuario(UserMixin,db.Model):
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


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField('Senha', validators=[validators.DataRequired()])
    submit = SubmitField('Login')



@app.route("/")
@login_required
def index():
    nome=current_user.nome
    return render_template('index.html', nome=nome)


@app.route("/login", methods=["POST"])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).all()[0]
        senha = form.password.data.encode('utf8')
        if usuario and bcrypt.checkpw(senha, usuario.senha):
            flash("Logado com Sucesso!", 'success')
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash("Login ou Senha Incorreta", 'danger')
            return redirect(url_for('login'))


@app.route("/login", methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route("/list")
@login_required
def listusers():
    content = {}
    return render_template('list.html')

@app.route("/new")
@login_required
def adduser():
    content = {}
    return render_template('adduser.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
from flask import Blueprint,render_template,redirect,url_for,flash
from facelock import db
from facelock.models import Usuario
from facelock.auth.forms import LoginForm
from flask_login import login_required, current_user, login_user, logout_user
import bcrypt


auth_blueprint = Blueprint('auth',__name__,template_folder='templates/auth')


@auth_blueprint.route("/login", methods=["POST"])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).all()[0]
        senha = form.password.data.encode('utf-8')
        if usuario and bcrypt.checkpw(senha, usuario.senha):
            flash("Logado com Sucesso!", 'success')
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash("Login ou Senha Incorreta", 'danger')
            return redirect(url_for('auth.login'))
    for fieldName, errorMessage in form.errors.items():
        for err in errorMessage:
            flash(err, 'danger')
    return render_template('login.html', form=form)


@auth_blueprint.route("/login", methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)



@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

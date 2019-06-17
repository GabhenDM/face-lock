from flask import Blueprint,render_template,redirect,url_for,flash, request
from facelock import db
from facelock.models import Usuario
from flask_login import login_required, current_user
from facelock.home.forms import RegisterForm


home_blueprint = Blueprint('home',__name__,template_folder='templates/home')



@home_blueprint.route("/list")
@login_required
def listusers():
    usuarios = Usuario.query.all()
    return render_template('list.html', usuarios=usuarios)


@home_blueprint.route("/new")
@login_required
def add():
    content = {}
    return render_template('add.html')

@home_blueprint.route("/edit/<string:id>", methods=['GET','POST'])
@login_required
def edit(id):
    form = RegisterForm()
    if request.method == 'GET':
        usuario = Usuario.query.get(id)
        if usuario:
            return render_template('edit.html', usuario=usuario, form=form)
    elif request.method == 'POST':
        usuario = Usuario.query.get(id)
       # usuario.nome = form.nome.data
        #usuario.email = form.email.data
        #usuario.is_admin = form.is_admin.data


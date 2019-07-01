from flask import Blueprint,render_template,redirect,url_for,flash, request
from facelock import db
from facelock.models import Usuario
from flask_login import login_required, current_user
from facelock.home.forms import RegisterForm, EditForm
from scripts.encode import encode
from werkzeug.utils import secure_filename
import bcrypt
import os


home_blueprint = Blueprint('home',__name__,template_folder='templates/home')

encodings = {}

def cacheEncodings():
    usuarios = Usuario.query.all()
    for usuario in usuarios:
        encodings.update((usuario.nome,usuario.encoding))



@home_blueprint.route("/list")
@login_required
def listusers():
    usuarios = Usuario.query.all()
    return render_template('list.html', usuarios=usuarios)


@home_blueprint.route("/new",methods=['GET','POST'])
@login_required
def add():
    form = RegisterForm(active=True)
    if request.method == "GET":
        return render_template('add.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            usuario_encontrado = Usuario.query.filter_by(email=form.email.data).all()
            if not usuario_encontrado:
                f = form.photo.data
                filename = secure_filename(f.filename)
                f.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','training_images',form.nome.data+'.jpg')))
                usuario =  Usuario(form.nome.data,form.email.data,bcrypt.hashpw(form.password.data.encode('utf8'), bcrypt.gensalt()), form.is_admin.data, form.ativo.data)
                db.session.add(usuario)
                db.session.commit()
                flash("Usuário Incluído com sucesso", 'success')
                encode()
                cacheEncodings()
                return redirect(url_for('home.listusers'))
            else:
                flash('Email já cadastrado', 'danger')
        for fieldName, errorMessage in form.errors.items():
            for err in errorMessage:
                print(fieldName)
                flash(err, 'danger')
        return render_template('add.html', form=form)


@home_blueprint.route("/edit/<string:id>", methods=['GET','POST'])
@login_required
def edit(id):
    if request.method == 'GET':
        usuario = Usuario.query.get(id)
        form = EditForm(obj=usuario)
        if usuario:
            return render_template('edit.html', usuario=usuario, form=form)
    elif request.method == 'POST':
        print('Entrou')
        form = EditForm()
        usuario = Usuario.query.get(id)
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.is_admin = form.is_admin.data
        usuario.ativo = form.ativo.data
        db.session.add(usuario)
        db.session.commit()
        flash("Usuário Alterado com sucesso", 'success')
        return redirect(url_for('home.listusers'))

@home_blueprint.route("/delete/<string:id>", methods=['GET'])
@login_required
def delete(id):
    if request.method == 'GET':
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            try:
                os.remove(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','training_images',usuario.nome+'.jpg')))
            except:
                flash("Nenhuma imagem associada ao usuario", "warning")
            db.session.commit()
            flash("Usuário removido com sucesso!", "danger")
            encode()
            return redirect(url_for('home.listusers'))
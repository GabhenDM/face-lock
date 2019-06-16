from flask import Blueprint,render_template,redirect,url_for,flash
from facelock import db
from facelock.models import Usuario
from flask_login import login_required, current_user


home_blueprint = Blueprint('home',__name__,template_folder='templates/home')



@home_blueprint.route("/list")
@login_required
def listusers():
    content = {}
    return render_template('list.html')


@home_blueprint.route("/new")
@login_required
def adduser():
    content = {}
    return render_template('adduser.html')

import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'SecretTestKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from facelock.models import Usuario

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from facelock.auth.views import auth_blueprint
from facelock.home.views import home_blueprint


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

app.register_blueprint(auth_blueprint,url_prefix="/auth")
app.register_blueprint(home_blueprint,url_prefix="/home")


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'SecretTestKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



from facelock.models import Usuario,Role

user_datastore = SQLAlchemySessionUserDatastore(db,
                                                Usuario,Role)
security = Security(app, user_datastore)


from facelock.auth.views import auth_blueprint
from facelock.home.views import home_blueprint

app.register_blueprint(auth_blueprint,url_prefix="/auth")
app.register_blueprint(home_blueprint,url_prefix="/home")


from facelock import db
from flask_security import UserMixin,RoleMixin

class RolesUsuarios(db.Model):
    __tablename__ = 'roles_usuarios'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('usuario_id', db.Integer(), db.ForeignKey('usuario.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    senha = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_usuarios',
                         backref=db.backref('usuarios', lazy='dynamic'))


    def __init__(self, nome, email, senha, is_admin, active):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.is_admin = is_admin
        self.active = active

    def __repr__(self):
        return f"Usuário {self.nome} - Email {self.email}"


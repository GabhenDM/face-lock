from flask_login import UserMixin
from facelock import db

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    senha = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)
    ativo = db.Column(db.Boolean)
    encoding = db.Column(db.LargeBinary)

    def __init__(self, nome, email, senha, is_admin, encoding, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.is_admin = is_admin
        self.ativo = ativo
        self.encoding = encoding

    def __repr__(self):
        return f"Usuário {self.nome} - Email {self.email}"
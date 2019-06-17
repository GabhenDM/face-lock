from facelock import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    senha = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)

    def __init__(self, nome, email, senha, is_admin):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.is_admin = is_admin

    def __repr__(self):
        return f"Usuário {self.nome} - Email {self.email}"


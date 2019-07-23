from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[validators.DataRequired()])
    email = StringField("Email", validators=[
                        validators.DataRequired(), validators.Email()])
    password = PasswordField('Senha', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Senhas devem ser iguais')
    ])
    confirm = PasswordField('Repita a Senha')
    is_admin = BooleanField('Administrador')
    ativo = BooleanField('Acesso Ativo?')
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Registrar')


class EditForm(FlaskForm):
    nome = StringField('Nome', validators=[validators.DataRequired()])
    email = StringField("Email", validators=[
                        validators.DataRequired(), validators.Email()])
    is_admin = BooleanField('Administrador')
    ativo = BooleanField("Acesso Ativo?")
    submit = SubmitField('Editar')


class PortaForm(FlaskForm):
    submit = SubmitField("Abrir Porta")

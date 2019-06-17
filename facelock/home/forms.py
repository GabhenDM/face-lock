from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,validators, PasswordField, BooleanField

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[validators.DataRequired()])
    email = StringField("Email", validators=[
                        validators.DataRequired(), validators.Email()])
    is_admin = BooleanField('Administrador', validators=[validators.DataRequired()])
    submit = SubmitField('Editar')

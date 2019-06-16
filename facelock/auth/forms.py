from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,validators, PasswordField

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        validators.DataRequired(), validators.Email()])
    password = PasswordField('Senha', validators=[validators.DataRequired()])
    submit = SubmitField('Login')

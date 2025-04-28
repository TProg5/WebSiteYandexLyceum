from flask_wtf import FlaskForm

from wtforms import (
    EmailField, PasswordField,
    BooleanField, SubmitField
)

from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
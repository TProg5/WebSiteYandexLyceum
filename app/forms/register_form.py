from flask_wtf import FlaskForm
from wtforms import (
    PasswordField, StringField, 
    TextAreaField, SubmitField,
    EmailField
)

from wtforms.validators import DataRequired
from wtforms.validators import Email, EqualTo

class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])

    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(),
            EqualTo('password', message="Пароли не совпадают")
        ]
    )

    submit = SubmitField("Зарегистрироваться")

from flask import Flask
from flask import render_template
from flask import redirect
from flask import session
from flask import request, make_response

from flask_login import login_required, logout_user
from flask_login import login_user, current_user

from forms.register_form import RegisterForm
from forms.login_form import LoginForm


from database.requests.user_requests import (
    add_user, check_email,
    returning_info_to_login
)


from database.requests.user_requests import login_manager, load_user


app = Flask(__name__)


app.secret_key = 'your_secret_key'  # Нужно для flash-сообщений и сессий


@app.route('/main', methods=['GET'])
def main():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        return render_template("info.html", current_user=current_user)

    return render_template("info.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    print(form.email.data)
    print(form.password.data)
    print(form.name.data)
    
    if request.method == 'POST':
        password: str = form.password.data
        password_again: str = form.password_again.data

        # Проверка на совпадение паролей
        if password != password_again:
            return render_template(
                "register.html", 
                message="Ошибка регистрации", 
                error="Пароли не совпадают",
                form=form
            )
    
    if form.validate_on_submit():

        print("TRUE")

        name: str = form.name.data
        email: str = form.email.data
        
        # проверка на существование почты
        if check_email(email=email):
            return render_template(
                "register.html", 
                message="Ошибка регистрации", 
                error="Такая почта уже зарегестрирована",
                form=form
            )
    
        add_user(
            username=name,
            email=email,
            hashed_password=password
        )
        
        print("TRue")
 
        return redirect('/login')

    session.pop('message', None)
    session.pop('error', None)

    # Если что-то не так — форма с ошибками будет показана снова
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        print("checkpoint - 1")
        email = form.email.data

        user = returning_info_to_login(email=email)

        print("checkpoint - 2")
        if user:
            print("checkpoint - 3")
            login_user(user=user, remember=form.remember_me.data)
            print("checkpoint - 4")

            return redirect("/dashboard")

        return render_template(
            'login.html',
            message="Ошибка Авторизации",
            error="Неправильный логин или пароль",
            form=form
        )

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


def main(app: Flask) -> None:
    login_manager.init_app(app=app)

    app.run(port=8080, host="127.0.0.1", debug=True)


if __name__ == "__main__":
    main(app=app)

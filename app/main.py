from flask import Flask
from flask import render_template
from flask import redirect
from flask import session
from flask import request, make_response

from flask_login import login_required, logout_user

from forms.register_form import RegisterForm
from forms.login_form import LoginForm

from database.requests.user_requests import add_user, check_email


from database.requests.user_requests import login_manager


app = Flask(__name__)


app.secret_key = 'your_secret_key'  # Нужно для flash-сообщений и сессий

app.route("/")
def main():
    return "Главная страница"


@app.route('/register', methods=['GET', 'POST'])
async def register():
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
        if await check_email(email=email):
            return render_template(
                "register.html", 
                message="Ошибка регистрации", 
                error="Такая почта уже зарегестрирована",
                form=form
            )
    
        await add_user(
            username=name,
            email=email,
            hashed_password=password
        )
        
        print("TRue")
        # Всё прошло — регистрируем
        return redirect('/login')

    session.pop('message', None)
    session.pop('error', None)

    # Если что-то не так — форма с ошибками будет показана снова
    return render_template('register.html', form=form)


@app.route("/login")
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        pass

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/main")
def main_page():
    return "You login"


def main(app: Flask) -> None:
    login_manager.init_app(app=app)

    app.run(port=8080, host="127.0.0.1", debug=True)


if __name__ == "__main__":
    main(app=app)

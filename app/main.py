from flask import Flask
from flask import render_template
from flask import redirect
from flask import session
from flask import request, make_response
from flask import url_for, abort

from flask_login import login_required, logout_user
from flask_login import login_user, current_user

from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm

from app.database.requests.user_requests import (
    add_user, check_email,
    returning_info_to_login
)


from app.database.requests.user_requests import login_manager, load_user

from app.auto_api import auto


from waitress import serve

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route("/")

@app.route("/", methods=["GET", "POST"])
def main():

    if current_user.is_authenticated:
        return render_template(
            "main_page.html", 
            current_user=current_user
        )
    
    return render_template("main_page.html")


# Функция для регистрации аккаунта, никак не изменяем
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

    return render_template('register.html', form=form)


# Функция для входа в аккаунт, никак не изменяем
@app.route("/login", methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data

        user = returning_info_to_login(email=email)

        if user:
            login_user(user=user, remember=form.remember_me.data)
            return redirect("/")

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


@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        return render_template("info.html", current_user=current_user)

    return render_template("info.html")


@app.route("/search-car", methods=["POST"])
def search_car():
    brand = request.form.get("brand")
    model = request.form.get("model")

    if not brand or not model:
        abort(400, "Марка и модель обязательны")

    return redirect(url_for('auto.get_auto_detail', brand=brand.lower(), model=model.lower()))


@app.route("/disclaimer", methods=["GET"])
def disclaimer():
    return render_template("disclaimer.html")


@app.template_filter('format_price')
def format_price(value):
    if value is None:
        return ""
    return f"{int(value):,}".replace(",", " ")


if __name__ == "__main__":
    login_manager.init_app(app=app)
    app.register_blueprint(auto)

    serve(app=app, port=8080, host="127.0.0.1")
    # port = int(os.environ.get("PORT", 8080))
    # app.run(host='0.0.0.0', port=port, debug=True)

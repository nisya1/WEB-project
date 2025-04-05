import flask
from flask import render_template, request, session, redirect, url_for, flash

from data.db_session import global_init, create_session
from data.users_models.users import Users

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/register', methods=['GET', 'POST'])
def register_form():
    if request.method == 'POST':
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password == confirm_password:
            user_exist = False
            global_init(f"database/users.db")
            sess1 = create_session()

            if sess1.query(Users).filter(Users.Name == name).first():
                flash('Такой пользователь с таким именем существует', 'error')
                user_exist = True
            if sess1.query(Users).filter(Users.Email == email).first():
                flash('Данная электронная почта уже привязана', 'error')
                user_exist = True

            if not user_exist:
                user = Users(
                    Name=name,
                    Email=email,
                    Password=password
                )

                sess1.add(user)
                sess1.commit()

                session["name"] = name
                session["email"] = email
                session["password"] = password
                session["user_active"] = True
                session["role"] = 2

                return redirect(url_for('to_movies'))

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        global_init(f"database/users.db")
        sess1 = create_session()
        user = sess1.query(Users).filter(Users.Email == email).first()

        if user:
            if user.Password == password:
                session["name"] = user.Name
                session["email"] = email
                session["password"] = password
                session["user_active"] = True
                session["role"] = user.RoleId

                return redirect(url_for('to_movies'))

            else:
                flash('Пароль неверный', 'error')
        else:
            flash('Пользователя с такой почтой не существует', 'error')

    return render_template('auth/login.html')


@bp.route('/logout', methods=['POST'])
def logout():
    if 'confirm_logout' in request.form:
        # Реальная логика выхода
        session.clear()
        return redirect(url_for('to_movies'))
    elif 'show_modal' in request.form:
        # Показываем страницу с модальным окном
        session["show_modal"] = True
        return redirect(url_for('to_movies'))

    session["show_modal"] = False
    return redirect(url_for('to_movies'))


@bp.route('/profile', methods=['POST'])
def profile():
    params = {
        "username": session["name"],
        "email": session["email"],
        "tickets": False,
        "is_admin": session["role"] == 1
    }
    return render_template("auth/profile.html", **params)

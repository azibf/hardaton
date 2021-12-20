from data import db_session
import os
from flask_ngrok import run_with_ngrok
from data.users1 import User
from flask import Flask, render_template, redirect, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    IntegerField, DateField, TextAreaField,  SelectField, FileField
from wtforms.validators import DataRequired, InputRequired, Length
from wtforms.fields.html5 import EmailField
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests
import sys


app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class InformationForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronimic = StringField('Отчество', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    work_experience = IntegerField('Рабочий стаж', validators=[DataRequired()])
    driver_license = IntegerField('Водительская лицензия', validators=[DataRequired()])
    comment = TextAreaField('Комментарии по состоянию здоровья', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class ChangeForm(FlaskForm):
    doctor_comment = TextAreaField('Заключение врача', validators=[DataRequired()])
    allow = StringField('Разрешение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronimic = StringField('Отчество', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    work_experience = IntegerField('Рабочий стаж', validators=[DataRequired()])
    driver_license = IntegerField('Водительская лицензия', validators=[DataRequired()])
    comment = TextAreaField('Комментарии по состоянию здоровья', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Проверка пароля', validators=[DataRequired()])
    submit = SubmitField('Зерегистрироваться')


class RegisterFormDoctor(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronimic = StringField('Отчество', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Проверка пароля', validators=[DataRequired()])
    submit = SubmitField('Зерегистрироваться')


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Hello')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            print(user.is_doctor)
            if user.is_doctor == 0:
                return redirect("/lk")
            else:
                return redirect("/drivers")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register/<int:is_driver>', methods=['GET', 'POST'])
def reqister(is_driver):
    logout_user()
    if is_driver:
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают", is_driver=is_driver)
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть", is_driver=is_driver)
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                patronimic=form.surname.data,
                age=form.age.data,
                work_experience=form.work_experience.data,
                driver_license=form.driver_license.data,
                comment=form.comment.data,
                email=form.email.data,
                pressure=0,
                pulse=0,
                temperature=0,
                reaction=0,
                sobriety=0,
                doctor_comment='',
                is_ready=0,
                doctor_id=1,
                hashed_password=form.password.data,
                is_doctor=0
            )
            session.add(user)
            session.commit()
            return redirect('/login')
    else:
        form = RegisterFormDoctor()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают", is_driver=is_driver)
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть", is_driver=is_driver)
            doctor = User(
                name=form.name.data,
                surname=form.surname.data,
                patronimic=form.surname.data,
                email=form.email.data,
                hashed_password=form.password.data,
                age=0,
                work_experience=0,
                driver_license=0,
                comment='',
                pressure=0,
                pulse=0,
                temperature=0,
                reaction=0,
                sobriety=0,
                doctor_comment='',
                is_ready=0,
                doctor_id=1,
                is_doctor=1
            )

            session.add(doctor)
            session.commit()
            return redirect('/login')
    return render_template('register.html', title='register', form=form, is_driver=is_driver)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/lk')
def user_information():
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    session = db_session.create_session()
    doctor = session.query(User).filter(User.id == user.doctor_id).first()
    return render_template('lk.html', title='lk', user=user, doctor=doctor)


@app.route('/change_information', methods=['GET', 'POST'])
@login_required
def change_info():
    form = InformationForm()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    if request.method == "GET":
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.patronimic.data = user.patronimic
            form.age.data = user.age
            form.work_experience.data = user.work_experience
            form.driver_license.data = user.driver_license
            form.comment.data = user.comment
        else:
            abort(404)
    if form.validate_on_submit():
        if user:
            user.name = form.name.data
            user.surname = form.surname.data
            user.patronimic = form.patronimic.data
            user.age = form.age.data
            user.work_experience = form.work_experience.data
            user.driver_license = form.driver_license.data
            user.comment = form.comment.data
            session.commit()
            return redirect('/lk')
        else:
            abort(404)
    return render_template('information.html', title='Редактирование информации', form=form)


@app.route("/drivers", methods=['GET', 'POST'])
def library():
    session = db_session.create_session()
    users = session.query(User).all()
    return render_template("drivers.html", title='Список водителей', users=users)


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_user(id):
    form = ChangeForm()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if request.method == "GET":
        if user:
            form.allow.data = "Разрешение получено" if user.is_ready == 1 else "Нет разрешения"
            form.doctor_comment.data = user.doctor_comment
        else:
            abort(404)
    if form.validate_on_submit():
        if user:
            user.is_ready = 1 if ("Есть разрешение" == form.allow.data) else 0
            user.doctor_comment = form.doctor_comment.data
            user.doctor_id = current_user.id
            session.commit()
            return redirect('/drivers')
        else:
            abort(404)
    return render_template('change.html', title='Редактирование разрешения', form=form, user=user)


if __name__ == '__main__':
    db_session.global_init("db/drivers.sqlite")
    app.run()
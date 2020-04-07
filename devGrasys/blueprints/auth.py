# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login

from devGrasys.forms.auth import RegisterFormStudent, RegisterFormAssistant, RegisterFormLecturer
from devGrasys.extensions import db
from devGrasys.models import Student, Assistant, Lecturer
from devGrasys.settings import Operations

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')


@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterFormStudent()
    if form.validate_on_submit():
        name = form.name.data
        user_id = form.user_id.data
        password = form.password.data
        user = Student(user_id=user_id, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('auth/register_student.html', form=form)


@auth_bp.route('/register/assistant', methods=['GET', 'POST'])
def register_assistant():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterFormAssistant()
    if form.validate_on_submit():
        name = form.name.data
        user_id = form.user_id.data
        password = form.password.data
        user = Assistant(user_id=user_id, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('auth/register_assistant.html', form=form)


@auth_bp.route('/register/lecturer', methods=['GET', 'POST'])
def register_lecturer():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterFormLecturer()
    if form.validate_on_submit():
        name = form.name.data
        user_id = form.user_id.data
        password = form.password.data
        user = Lecturer(user_id=user_id, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('auth/register_lecturer.html', form=form)

# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, current_user

from devGrasys.models import Student
from devGrasys.forms.student import RegisterFormStudent, LoginFormStudent
from devGrasys.utils import redirect_back
from devGrasys.extensions import db

student_bp = Blueprint('student', __name__)


@student_bp.route('/student', methods=['GET'])
def index_student():
    return render_template('student/index_student.html')


@student_bp.route('/student/login', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginFormStudent()
    if form.validate_on_submit():
        user = Student.query.filter_by(user_id=form.user_id.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect_back()
            else:
                flash('Your account is blocked.', 'warning')
                return redirect(url_for('main.index'))
        flash('Invalid userID or password.', 'warning')

    return render_template('student/login_student.html', form=form)


@student_bp.route('/student/register', methods=['GET', 'POST'])
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
        return redirect(url_for('.login_student'))
    return render_template('student/register_student.html', form=form)

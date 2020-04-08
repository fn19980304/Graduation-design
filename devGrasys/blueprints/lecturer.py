# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login_multi import login_user, current_user

from devGrasys.models import Lecturer
from devGrasys.forms.lecturer import RegisterFormLecturer, LoginFormLecturer
from devGrasys.utils import redirect_back
from devGrasys.extensions import db

lecturer_bp = Blueprint('lecturer', __name__)


@lecturer_bp.route('/student', methods=['GET'])
def index_lecturer():
    return render_template('lecturer/index_lecturer.html')


@lecturer_bp.route('/lecturer/login', methods=['GET', 'POST'])
def login_lecturer():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginFormLecturer()
    if form.validate_on_submit():
        user = Lecturer.query.filter_by(user_id=form.user_id.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect_back()
            else:
                flash('Your account is blocked.', 'warning')
                return redirect(url_for('main.index'))
        flash('Invalid userID or password.', 'warning')

    return render_template('lecturer/login_lecturer.html', form=form)


@lecturer_bp.route('/lecturer/register', methods=['GET', 'POST'])
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
        return redirect(url_for('.login_lecturer'))
    return render_template('lecturer/register_lecturer.html', form=form)

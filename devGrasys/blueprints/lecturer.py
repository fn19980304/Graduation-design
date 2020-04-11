# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask import render_template, flash, redirect, url_for, Blueprint, send_from_directory, current_app
from flask_login import login_required, login_user, logout_user, current_user

from devGrasys.models import Lecturer, Course
from devGrasys.forms.lecturer import RegisterFormLecturer, LoginFormLecturer, CreateCourseForm
from devGrasys.utils import redirect_back
from devGrasys.extensions import db

lecturer_bp = Blueprint('lecturer', __name__)


@lecturer_bp.route('/', methods=['GET'])
def index_lecturer():
    if current_user.is_authenticated:
        user = current_user
        courses = Course.query.filter_by(lecturer=user).all()
        return render_template('lecturer/index_lecturer.html', courses=courses)
    return render_template('lecturer/index_lecturer.html')


@lecturer_bp.route('/login', methods=['GET', 'POST'])
def login_lecturer():
    if current_user.is_authenticated:
        return redirect(url_for('lecturer.index_lecturer'))

    form = LoginFormLecturer()
    if form.validate_on_submit():
        user = Lecturer.query.filter_by(user_id=form.user_id.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect(url_for('lecturer.index_lecturer'))
        flash('Invalid userID or password.', 'warning')

    return render_template('lecturer/login_lecturer.html', form=form)


@lecturer_bp.route('/logout')
@login_required
def logout_lecturer():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('main.index'))


@lecturer_bp.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('lecturer.login_lecturer'))
    return render_template('lecturer/register_lecturer.html', form=form)


@lecturer_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@lecturer_bp.route('/create', methods=['GET', 'POST'])
def create_course():
    form = CreateCourseForm()
    user = current_user
    if form.validate_on_submit():
        name = form.name.data
        intro = form.intro.data
        course = Course(name=name, intro=intro)
        user.courses.append(course)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('lecturer.index_lecturer'))
    return render_template('lecturer/create_course.html', form=form)


@lecturer_bp.route('/<course_name>')
def admin_course(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    return render_template('lecturer/admin_course.html', course=course)

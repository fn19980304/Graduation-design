# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask import render_template, flash, redirect, url_for, Blueprint, send_from_directory, current_app
from flask_login import login_user, current_user, login_required, logout_user

from devGrasys.models import Student, Course, Lecturer
from devGrasys.forms.student import RegisterFormStudent, LoginFormStudent
from devGrasys.utils import redirect_back
from devGrasys.extensions import db

student_bp = Blueprint('student', __name__)


@student_bp.route('', methods=['GET'])
def index_student():
    if current_user.is_authenticated:
        courses = Course.query.all()
        lecturers = Lecturer.query.all()
        return render_template('student/index_student.html', courses=courses, lecturers=lecturers)
    return render_template('student/index_student.html')


@student_bp.route('/login', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('student.index_student'))

    form = LoginFormStudent()
    if form.validate_on_submit():
        user = Student.query.filter_by(user_id=form.user_id.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect_back()
        flash('Invalid userID or password.', 'warning')

    return render_template('student/login_student.html', form=form)


@student_bp.route('/logout')
@login_required
def logout_student():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('main.index'))


@student_bp.route('/register', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('student.index_student'))

    form = RegisterFormStudent()
    if form.validate_on_submit():
        name = form.name.data
        user_id = form.user_id.data
        password = form.password.data
        user = Student(user_id=user_id, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('student.login_student'))
    return render_template('student/register_student.html', form=form)


@student_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@student_bp.route('/<course_name>')
def view_course(course_name):
    student = current_user
    course = Course.query.filter_by(name=course_name).first_or_404()
    return render_template('student/view_course.html', course=course, student=student)


@student_bp.route('/<course_name>/join', methods=['POST'])
def join_course(course_name):
    student = current_user
    course = Course.query.filter_by(name=course_name).first_or_404()
    if course.student_is_joined(student=student):
        flash('Already joined.', 'info')
        return redirect_back()

    course.student_join(student)
    flash('Course joined.', 'success')
    return redirect_back()


@student_bp.route('/<course_name>/quit', methods=['POST'])
def quit_course(course_name):
    student = current_user
    course = Course.query.filter_by(name=course_name).first_or_404()
    if not course.student_is_joined(student=student):
        flash('Not joined yet.', 'info')
        return redirect_back()

    course.student_quit(student)
    flash('Course quoted.', 'success')
    return redirect_back()

# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask import render_template, flash, redirect, url_for, Blueprint, send_from_directory, current_app
from flask_login import login_user, current_user, login_required, logout_user

from devGrasys.models import Assistant, Course, Lecturer, Homework, Answer, Student, Correct
from devGrasys.forms.assistant import RegisterFormAssistant, LoginFormAssistant, CorrectHomeworkForm
from devGrasys.utils import redirect_back
from devGrasys.extensions import db

assistant_bp = Blueprint('assistant', __name__)


@assistant_bp.route('/', methods=['GET'])
def index_assistant():
    if current_user.is_authenticated:
        courses = Course.query.all()
        lecturers = Lecturer.query.all()
        return render_template('assistant/index_assistant.html', courses=courses, lecturers=lecturers)
    return render_template('assistant/index_assistant.html')


@assistant_bp.route('/login', methods=['GET', 'POST'])
def login_assistant():
    if current_user.is_authenticated:
        return redirect(url_for('assistant.index_assistant'))

    form = LoginFormAssistant()
    if form.validate_on_submit():
        user = Assistant.query.filter_by(user_id=form.user_id.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect_back()
        flash('Invalid userID or password.', 'warning')

    return render_template('assistant/login_assistant.html', form=form)


@assistant_bp.route('/logout')
@login_required
def logout_assistant():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('main.index'))


@assistant_bp.route('/register', methods=['GET', 'POST'])
def register_assistant():
    if current_user.is_authenticated:
        return redirect(url_for('assistant.index_assistant'))

    form = RegisterFormAssistant()
    if form.validate_on_submit():
        name = form.name.data
        user_id = form.user_id.data
        password = form.password.data
        user = Assistant(user_id=user_id, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('assistant.login_assistant'))
    return render_template('assistant/register_assistant.html', form=form)


@assistant_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@assistant_bp.route('/<course_name>')
def view_course(course_name):
    assistant = current_user
    course = Course.query.filter_by(name=course_name).first_or_404()
    return render_template('assistant/view_course.html', course=course, assistant=assistant)


@assistant_bp.route('/<course_name>/join', methods=['POST'])
def join_course(course_name):
    assistant = current_user
    course = Course.query.filter_by(name=course_name).first_or_404()
    if course.assistant_is_joined(assistant=assistant):
        flash('Already joined.', 'info')
        return redirect_back()

    course.assistant_join(assistant)
    flash('Course joined.', 'success')
    return redirect_back()


@assistant_bp.route('/<course_name>/quit', methods=['POST'])
def quit_course(course_name):
    assistant = current_user
    course = Course.query.filter_by(name=course_name).first_or_404()
    if not course.assistant_is_joined(assistant=assistant):
        flash('Not joined yet.', 'info')
        return redirect_back()

    course.assistant_quit(assistant)
    flash('Course quoted.', 'success')
    return redirect_back()


@assistant_bp.route('/select', methods=['GET'])
def select_course():
    assistant = current_user
    courses = Course.query.all()
    return render_template('assistant/select_course.html', courses=courses, assistant=assistant)


@assistant_bp.route('/select/<course_name>', methods=['GET'])
def view_list(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    homework_group = Homework.query.filter_by(course=course)
    return render_template('assistant/view_list.html', course=course, homework_group=homework_group)


@assistant_bp.route('/select/<course_name>/<homework_title>', methods=['GET'])
def view_homework(course_name, homework_title):
    course = Course.query.filter_by(name=course_name).first_or_404()
    homework = Homework.query.filter_by(course=course).filter_by(title=homework_title).first_or_404()
    answers = Answer.query.filter_by(homework=homework)
    return render_template('assistant/view_homework.html', course=course, homework=homework, answers=answers)


@assistant_bp.route('/select/<course_name>/<homework_title>/<student_name>', methods=['GET', 'POST'])
def correct_homework(course_name, homework_title, student_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    homework = Homework.query.filter_by(course=course).filter_by(title=homework_title).first_or_404()
    student = Student.query.filter_by(name=student_name).first_or_404()
    answer = Answer.query.filter_by(homework=homework).filter_by(student=student).first_or_404()
    form = CorrectHomeworkForm()
    if not answer.is_corrected() and form.validate_on_submit():
        body = form.body.data
        grade = form.grade.data
        correct = Correct(body=body, grade=grade)
        homework.corrects.append(correct)
        answer.correct.append(correct)
        db.session.add(correct)
        db.session.commit()
        return redirect_back(
            url_for('assistant.correct_homework', course_name=course.name, homework_title=homework.title,
                    student_name=student.name))
    correct = Correct.query.filter_by(answer=answer).first()
    return render_template('assistant/correct_homework.html', correct=correct, answer=answer, student=student,
                           homework=homework,
                           form=form)

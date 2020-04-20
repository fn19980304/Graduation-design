# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask import render_template, flash, redirect, url_for, Blueprint, send_from_directory, current_app
from flask_login import login_user, current_user, login_required, logout_user

from devGrasys.models import Student, Course, Homework, Answer, Correct
from devGrasys.forms.student import RegisterFormStudent, LoginFormStudent, AnswerForm, EditProfileStudentForm, \
    UploadAvatarStudentForm, CropAvatarStudentForm
from devGrasys.utils import redirect_back, flash_errors
from devGrasys.extensions import db, avatars

student_bp = Blueprint('student', __name__)


@student_bp.route('', methods=['GET'])
def index_student():
    if current_user.is_authenticated:
        courses = Course.query.all()
        return render_template('student/index_student.html', courses=courses)
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


@student_bp.route('/select', methods=['GET'])
def select_course():
    student = current_user
    courses = Course.query.all()
    return render_template('student/select_course.html', courses=courses, student=student)


@student_bp.route('/select/<course_name>', methods=['GET'])
def view_list(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    homework_group = Homework.query.filter_by(course=course)
    return render_template('student/view_list.html', course=course, homework_group=homework_group)


@student_bp.route('/select/<course_name>/<homework_title>', methods=['GET', 'POST'])
def view_homework(course_name, homework_title):
    student = current_user
    course = Course.query.filter_by(name=course_name).first_or_404()
    homework = Homework.query.filter_by(course=course).filter_by(title=homework_title).first_or_404()
    form = AnswerForm()
    if not homework.is_answered(student=student) and form.validate_on_submit():
        body = form.body.data
        answer = Answer(body=body)
        homework.answers.append(answer)
        student.answers.append(answer)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('student.view_homework', course_name=course.name, homework_title=homework.title))
    answer = homework.answers.filter_by(student=student).first()
    correct = Correct.query.filter_by(answer=answer).first()
    return render_template('student/view_homework.html', homework=homework, student=student, answer=answer,
                           correct=correct, form=form)


@student_bp.route('/settings/profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileStudentForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('student.index_student'))
    form.name.data = current_user.name
    return render_template('student/settings/edit_profile.html', form=form)


@student_bp.route('/settings/avatar')
def change_avatar():
    upload_form = UploadAvatarStudentForm()
    crop_form = CropAvatarStudentForm()
    return render_template('student/settings/change_avatar.html', upload_form=upload_form, crop_form=crop_form)


@student_bp.route('/settings/avatar/upload', methods=['POST'])
def upload_avatar():
    form = UploadAvatarStudentForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = avatars.save_avatar(image)
        current_user.avatar_raw = filename
        db.session.commit()
        flash('Image uploaded, please crop.', 'success')
    flash_errors(form)
    return redirect(url_for('.change_avatar'))


@student_bp.route('/settings/avatar/crop', methods=['POST'])
def crop_avatar():
    form = CropAvatarStudentForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        w = form.w.data
        h = form.h.data
        filenames = avatars.crop_avatar(current_user.avatar_raw, x, y, w, h)
        current_user.avatar_s = filenames[0]
        current_user.avatar_m = filenames[1]
        current_user.avatar_l = filenames[2]
        db.session.commit()
        flash('Avatar updated.', 'success')
    flash_errors(form)
    return redirect(url_for('.change_avatar'))

# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""
from datetime import datetime

from flask import render_template, flash, redirect, url_for, Blueprint, send_from_directory, current_app, request
from flask_login import login_required, login_user, logout_user, current_user

from devGrasys.models import Lecturer, Course, Homework, Student, Answer
from devGrasys.forms.lecturer import RegisterFormLecturer, LoginFormLecturer, CreateCourseForm, AdminCourseForm, \
    AssignHomeworkForm, EditProfileFormLecturer, CropAvatarFormLecturer, UploadAvatarFormLecturer
from devGrasys.utils import redirect_back, flash_errors
from devGrasys.extensions import db, avatars

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
                return redirect_back()
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
        return redirect(url_for('lecturer.index_lecturer'))

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
    lecturer = current_user
    if form.validate_on_submit():
        name = form.name.data
        intro = form.intro.data
        lecturer_name = lecturer.name
        course = Course(name=name, intro=intro, lecturer_name=lecturer_name)
        lecturer.courses.append(course)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('lecturer.index_lecturer'))
    return render_template('lecturer/create_course.html', form=form)


@lecturer_bp.route('/<course_name>')
def view_course(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    return render_template('lecturer/view_course.html', course=course)


@lecturer_bp.route('/<course_name>/end', methods=['POST'])
def end_course(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    db.session.delete(course)
    db.session.commit()
    flash('Course ended.', 'success')
    return redirect(url_for('lecturer.index_lecturer'))


@lecturer_bp.route('/<course_name>/students')
def show_students(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['USER_PER_PAGE']
    pagination = course.students.paginate(page, per_page)
    students = pagination.items
    return render_template('lecturer/course_students.html', course=course, pagination=pagination, students=students)


@lecturer_bp.route('/<course_name>/assistants')
def show_assistants(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['USER_PER_PAGE']
    pagination = course.assistants.paginate(page, per_page)
    assistants = pagination.items
    return render_template('lecturer/course_assistants.html', course=course, pagination=pagination,
                           assistants=assistants)


@lecturer_bp.route('/<course_name>/admin', methods=['GET', 'POST'])
def edit_course(course_name):
    form = AdminCourseForm()
    course = Course.query.filter_by(name=course_name).first_or_404()
    if form.validate_on_submit():
        course.name = form.name.data
        course.intro = form.intro.data
        db.session.commit()
        flash('Updated success.', 'success')
        return redirect(url_for('lecturer.view_course', course_name=course.name))
    form.name.data = course.name
    form.intro.data = course.intro
    return render_template('lecturer/edit_course.html', form=form)


@lecturer_bp.route('/<course_name>/picture')
def change_picture(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    upload_form = UploadAvatarFormLecturer()
    crop_form = CropAvatarFormLecturer()
    return render_template('lecturer/change_picture.html', course=course, upload_form=upload_form, crop_form=crop_form)


@lecturer_bp.route('/<course_name>/picture/upload', methods=['POST'])
def upload_picture(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    form = UploadAvatarFormLecturer()
    if form.validate_on_submit():
        image = form.image.data
        filename = avatars.save_avatar(image)
        course.avatar_raw = filename
        db.session.commit()
        flash('Image uploaded, please crop.', 'success')
    flash_errors(form)
    return redirect(url_for('lecturer.change_picture', course_name=course.name))


@lecturer_bp.route('/<course_name>/picture/crop', methods=['POST'])
def crop_picture(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    form = CropAvatarFormLecturer()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        w = form.w.data
        h = form.h.data
        filenames = avatars.crop_avatar(course.avatar_raw, x, y, w, h)
        course.avatar_s = filenames[0]
        course.avatar_m = filenames[1]
        course.avatar_l = filenames[2]
        db.session.commit()
        flash('Picture updated.', 'success')
    flash_errors(form)
    return redirect(url_for('lecturer.change_picture', course_name=course.name))


@lecturer_bp.route('/select', methods=['GET'])
def select_course():
    user = current_user
    courses = Course.query.filter_by(lecturer=user).all()
    return render_template('lecturer/select_course.html', courses=courses)


@lecturer_bp.route('/select/<course_name>', methods=['GET', 'POST'])
def view_homework(course_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    homework_group = Homework.query.filter_by(course=course)
    form = AssignHomeworkForm()
    current_time = datetime.utcnow()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        new_homework = Homework(title=title, description=description, deadline=deadline)
        course.homework_group.append(new_homework)
        db.session.add(new_homework)
        db.session.commit()
        return redirect(url_for('lecturer.view_homework', course_name=course.name))
    return render_template('lecturer/view_homework.html', course=course, homework_group=homework_group, form=form,
                           current_time=current_time)


@lecturer_bp.route('/select/<course_name>/<homework_title>', methods=['GET'])
def check_homework(course_name, homework_title):
    course = Course.query.filter_by(name=course_name).first_or_404()
    students = course.students
    homework = Homework.query.filter_by(course=course).filter_by(title=homework_title).first_or_404()
    answers = homework.answers
    submitted_number = 0
    for student in students:
        if student.is_submitted(homework=homework):
            submitted_number += 1
    return render_template('lecturer/check_homework.html', course=course, homework=homework, students=students,
                           answers=answers,
                           submitted_number=submitted_number)


@lecturer_bp.route('/select/<course_name>/<homework_title>/<student_name>', methods=['GET'])
def check_student(course_name, homework_title, student_name):
    course = Course.query.filter_by(name=course_name).first_or_404()
    homework = Homework.query.filter_by(course=course).filter_by(title=homework_title).first_or_404()
    student = Student.query.filter_by(name=student_name).first_or_404()
    answer = Answer.query.filter_by(homework=homework).filter_by(student=student).first_or_404()
    return render_template('lecturer/check_student.html', homework=homework, answer=answer, student=student)


@lecturer_bp.route('/settings/profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileFormLecturer()
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('lecturer.index_lecturer'))
    form.name.data = current_user.name
    return render_template('lecturer/settings/edit_profile.html', form=form)


@lecturer_bp.route('/settings/avatar')
def change_avatar():
    upload_form = UploadAvatarFormLecturer()
    crop_form = CropAvatarFormLecturer()
    return render_template('lecturer/settings/change_avatar.html', upload_form=upload_form, crop_form=crop_form)


@lecturer_bp.route('/settings/avatar/upload', methods=['POST'])
def upload_avatar():
    form = UploadAvatarFormLecturer()
    if form.validate_on_submit():
        image = form.image.data
        filename = avatars.save_avatar(image)
        current_user.avatar_raw = filename
        db.session.commit()
        flash('Image uploaded, please crop.', 'success')
    flash_errors(form)
    return redirect(url_for('.change_avatar'))


@lecturer_bp.route('/settings/avatar/crop', methods=['POST'])
def crop_avatar():
    form = CropAvatarFormLecturer()
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

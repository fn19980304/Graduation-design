# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

import os
from datetime import datetime

from flask_login import UserMixin
from flask_avatars import Identicon
from werkzeug.security import generate_password_hash, check_password_hash

from devGrasys.extensions import db

course_student_table = db.Table('course_student', db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
                                db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
                                )

course_assistant_table = db.Table('course_assistant', db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
                                  db.Column('assistant_id', db.Integer, db.ForeignKey('assistant.id'))
                                  )


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))

    courses = db.relationship('Course', secondary=course_student_table, back_populates='students', lazy='dynamic')

    def get_id(self):
        return 'student.' + str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Assistant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))

    courses = db.relationship('Course', secondary=course_assistant_table, back_populates='assistants', lazy='dynamic')

    def get_id(self):
        return 'assistant.' + str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Lecturer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))

    courses = db.relationship('Course', back_populates='lecturer')

    def get_id(self):
        return 'lecturer.' + str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    lecturer_name = db.Column(db.String(30))
    intro = db.Column(db.Text)

    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))

    # 讲师对课程：一对多
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    lecturer = db.relationship('Lecturer', back_populates='courses')

    # 助教对课程：多对多
    assistants = db.relationship('Assistant', secondary=course_assistant_table, back_populates='courses',
                                 lazy='dynamic')

    # 学生对课程：多对多
    students = db.relationship('Student', secondary=course_student_table, back_populates='courses', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Course, self).__init__(**kwargs)
        self.generate_avatar()

    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.name)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    def student_join(self, student):
        if not self.student_is_joined(student):
            self.students.append(student)
            db.session.commit()

    def student_quit(self, student):
        if self.student_is_joined(student):
            self.students.remove(student)
            db.session.commit()

    def student_is_joined(self, student):
        return self.students.filter_by(id=student.id).first() is not None

    def assistant_join(self, assistant):
        if not self.assistant_is_joined(assistant):
            self.assistants.append(assistant)
            db.session.commit()

    def assistant_quit(self, assistant):
        if self.assistant_is_joined(assistant):
            self.assistants.remove(assistant)
            db.session.commit()

    def assistant_is_joined(self, assistant):
        return self.assistants.filter_by(id=assistant.id).first() is not None

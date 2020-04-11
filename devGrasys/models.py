# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

import os
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from devGrasys.extensions import db

student_class_table = db.Table('student_class', db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                               db.Column('class_id', db.Integer, db.ForeignKey('class.id')))

assistant_class_table = db.Table('assistant_class',
                                 db.Column('assistant_id', db.Integer, db.ForeignKey('assistant.id')),
                                 db.Column('class_id', db.Integer, db.ForeignKey('class.id')))


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))

    # classes = db.relationship('Class', secondary=student_class_table, back_populates='students')

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

    # classes = db.relationship('Class', secondary=assistant_class_table, back_populates='assistants')

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

    classes = db.relationship('Class', back_populates='lecturer')

    def get_id(self):
        return 'lecturer.' + str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Class(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    intro = db.Column(db.Text)

    # 学生对课程：多对多
    # students = db.relationship('Student', secondary=student_class_table, back_populates='classes')
    # 助教对课程：多对多
    # assistants = db.relationship('assistant', secondary=assistant_class_table, back_populates='classes')
    # 讲师对课程：一对多
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    lecturer = db.relationship('Lecturer', back_populates='classes')

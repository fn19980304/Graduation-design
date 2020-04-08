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


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))

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

    def get_id(self):
        return 'lecturer.' + str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

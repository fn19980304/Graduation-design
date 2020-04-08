# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError

from devGrasys.models import Lecturer


class LoginFormLecturer(FlaskForm):
    user_id = StringField('UserID', validators=[DataRequired(), Length(10, 10)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterFormLecturer(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    user_id = StringField('UserID', validators=[DataRequired(), Length(10, 10), Regexp('^[L][0-9]*$',
                                                                                       message='Lecturer ID should '
                                                                                               'begin with L.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_user_id(self, field):
        if Lecturer.query.filter_by(user_id=field.data).first():
            raise ValidationError('The ID is already in use.')

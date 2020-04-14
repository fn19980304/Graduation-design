# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms.fields.html5 import DateField

from devGrasys.models import Lecturer, Course


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


class CreateCourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    intro = TextAreaField('Introduction', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_class_name(self, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('The class name is already in use.')


class AdminCourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    intro = TextAreaField('Introduction', validators=[DataRequired()])
    submit = SubmitField()

    def validate_class_name(self, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('The class name is already in use.')


class AssignHomeworkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 30)])
    description = CKEditorField('Description', validators=[DataRequired()])
    deadline=DateField('Deadline',format='%Y-%m-%d')
    submit = SubmitField('Assign')

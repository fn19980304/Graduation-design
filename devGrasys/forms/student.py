# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError

from devGrasys.models import Student


class LoginFormStudent(FlaskForm):
    user_id = StringField('UserID', validators=[DataRequired(), Length(10, 10)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterFormStudent(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    user_id = StringField('UserID', validators=[DataRequired(), Length(10, 10), Regexp('^[S][0-9]*$',
                                                                                       message='Student ID should '
                                                                                               'begin with S.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_user_id(self, field):
        if Student.query.filter_by(user_id=field.data).first():
            raise ValidationError('The ID is already in use.')


class AnswerForm(FlaskForm):
    body = CKEditorField('Your answer:', validators=[DataRequired()])
    submit = SubmitField()


class EditProfileFormStudent(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()


class UploadAvatarFormStudent(FlaskForm):
    image = FileField('Upload', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField()


class CropAvatarFormStudent(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('Crop and Update')

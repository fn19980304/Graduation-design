# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError

from devGrasys.models import Assistant


class LoginFormAssistant(FlaskForm):
    user_id = StringField('UserID', validators=[DataRequired(), Length(10, 10)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterFormAssistant(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    user_id = StringField('UserID', validators=[DataRequired(), Length(10, 10), Regexp('^[A][0-9]*$',
                                                                                       message='Lecturer ID should '
                                                                                               'begin with A.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_user_id(self, field):
        if Assistant.query.filter_by(user_id=field.data).first():
            raise ValidationError('The ID is already in use.')


class CorrectHomeworkForm(FlaskForm):
    body = CKEditorField('Your remark to the answer:', validators=[DataRequired()])
    grade = SelectField('Answer grade:',
                        validators=[DataRequired()],
                        choices=[('A', 'A - Excellent'), ('B', 'B - Well'), ('C', 'C - Qualified'),
                                 ('D', 'D - Unqualified')],
                        )
    submit = SubmitField()


class EditProfileFormAssistant(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()


class UploadAvatarFormAssistant(FlaskForm):
    image = FileField('Upload', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField()


class CropAvatarFormAssistant(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('Crop and Update')

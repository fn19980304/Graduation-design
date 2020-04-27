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
    user_id = StringField('用户ID', validators=[DataRequired(), Length(10, 10)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterFormStudent(FlaskForm):
    name = StringField('用户名称', validators=[DataRequired(), Length(1, 30)])
    user_id = StringField('用户ID', validators=[DataRequired(), Length(10, 10), Regexp('^[S][0-9]*$',
                                                                                       message='Student ID should '
                                                                                               'begin with S.')])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_user_id(self, field):
        if Student.query.filter_by(user_id=field.data).first():
            raise ValidationError('ID已经被其他用户注册！')


class AnswerForm(FlaskForm):
    body = CKEditorField('你的答案：', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileFormStudent(FlaskForm):
    name = StringField('用户名称', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('更改')


class UploadAvatarFormStudent(FlaskForm):
    image = FileField('上传', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], '文件格式应为 .jpg 或 .png.')
    ])
    submit = SubmitField('上传')


class CropAvatarFormStudent(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('裁剪并上传')

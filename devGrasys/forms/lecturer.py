# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms.fields.html5 import DateField

from devGrasys.models import Lecturer, Course


class LoginFormLecturer(FlaskForm):
    user_id = StringField('用户ID', validators=[DataRequired(), Length(10, 10)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterFormLecturer(FlaskForm):
    name = StringField('用户名称', validators=[DataRequired(), Length(1, 30)])
    user_id = StringField('用户ID', validators=[DataRequired(), Length(10, 10), Regexp('^[L][0-9]*$',
                                                                                       message='Lecturer ID should '
                                                                                               'begin with L.')])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_user_id(self, field):
        if Lecturer.query.filter_by(user_id=field.data).first():
            raise ValidationError('ID已经被其他用户注册！')


class CreateCourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(1, 30)])
    intro = TextAreaField('课程介绍', validators=[DataRequired()])
    submit = SubmitField('创建')

    def validate_class_name(self, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('课程名已经被其他讲师使用！')


class AdminCourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(1, 30)])
    intro = TextAreaField('课程介绍', validators=[DataRequired()])
    submit = SubmitField('修改')

    def validate_class_name(self, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('课程名已经被其他讲师使用！')


class AssignHomeworkForm(FlaskForm):
    title = StringField('作业标题', validators=[DataRequired(), Length(1, 30)])
    description = CKEditorField('作业描述', validators=[DataRequired()])
    deadline = DateField('截止日期', format='%Y-%m-%d')
    submit = SubmitField('布置')


class EditProfileFormLecturer(FlaskForm):
    name = StringField('用户名称', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('修改')


class UploadAvatarFormLecturer(FlaskForm):
    image = FileField('上传', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], '文件格式应为 .jpg 或 .png.')
    ])
    submit = SubmitField('上传')


class CropAvatarFormLecturer(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('裁剪并上传')

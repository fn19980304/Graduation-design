# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError

from devGrasys.models import User


class RegisterForm(FlaskForm):
    """注册表单
    用户注册ID时，A代表助教账户，L代表讲师账户，S代表学生账户
    """
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    user_id = StringField('UserID', validators=[DataRequired(), Length(10, 10), Regexp('^[ALS][0-9]*$',
                                                                                       message='Your ID should start '
                                                                                               'with A,L or S and '
                                                                                               'followed by numbers')])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_user_id(self, field):
        if User.query.filter_by(user_id=field.data).first():
            raise ValidationError('The ID is already in use.')

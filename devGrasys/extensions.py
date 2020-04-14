# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login.login_manager import LoginManager
from flask_avatars import Avatars
from flask_moment import Moment
from flask_ckeditor import CKEditor

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
avatars = Avatars()
moment = Moment()
ckeditor = CKEditor()


@login_manager.user_loader
def load_user(user_id):
    temp = user_id.split('.')
    try:
        uid = temp[1]
        if temp[0] == 'student':
            from devGrasys.models import Student
            return Student.query.get(int(uid))
        elif temp[0] == 'assistant':
            from devGrasys.models import Assistant
            return Assistant.query.get(int(uid))
        else:
            from devGrasys.models import Lecturer
            return Lecturer.query.get(int(uid))
    except IndexError:
        return None

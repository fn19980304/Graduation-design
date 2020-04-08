# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login_multi import login_user, current_user

from devGrasys.models import Assistant
from devGrasys.forms.assistant import RegisterFormAssistant, LoginFormAssistant
from devGrasys.utils import redirect_back
from devGrasys.extensions import db

assistant_bp = Blueprint('assistant', __name__)


@assistant_bp.route('/student', methods=['GET'])
def index_assistant():
    return render_template('assistant/index_assistant.html')


@assistant_bp.route('/assistant/login', methods=['GET', 'POST'])
def login_assistant():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginFormAssistant()
    if form.validate_on_submit():
        user = Assistant.query.filter_by(user_id=form.user_id.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect_back()
            else:
                flash('Your account is blocked.', 'warning')
                return redirect(url_for('main.index'))
        flash('Invalid userID or password.', 'warning')

    return render_template('assistant/login_assistant.html', form=form)


@assistant_bp.route('/assistant/register', methods=['GET', 'POST'])
def register_assistant():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterFormAssistant()
    if form.validate_on_submit():
        name = form.name.data
        user_id = form.user_id.data
        password = form.password.data
        user = Assistant(user_id=user_id, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login_assistant'))
    return render_template('assistant/register_assistant.html', form=form)

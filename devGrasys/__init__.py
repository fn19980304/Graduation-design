# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""

import os
from flask import Flask

from devGrasys.blueprints.main import main_bp
from devGrasys.blueprints.student import student_bp
from devGrasys.blueprints.lecturer import lecturer_bp
from devGrasys.blueprints.assistant import assistant_bp
from devGrasys.extensions import db, bootstrap, login_manager, avatars
from devGrasys.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('devGrasys')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    avatars.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')
    app.register_blueprint(assistant_bp, url_prefix='/assistant')

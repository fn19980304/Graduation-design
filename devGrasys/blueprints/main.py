# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""
import os

from flask import Blueprint,render_template
from devGrasys.extensions import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    db.create_all()
    return render_template('main/index.html')

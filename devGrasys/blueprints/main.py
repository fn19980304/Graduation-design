# -*- coding: utf-8 -*-
"""
    :author: Jifan Jiang
    :url: https://github.com/fn19980304
"""
import os

from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return 'System Test!'

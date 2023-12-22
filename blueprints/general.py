from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify
from config.exts import db
from config.models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

from utils.captchas import getCaptchaPic

bp = Blueprint('general', __name__, url_prefix='/')


@bp.route('/getCaptchaImg', methods=['POST'])
def getCaptchaImg():
    file_name, coding = getCaptchaPic(request.form.get('coding'))
    return jsonify({'code': 200, 'src': file_name, 'coding': coding})

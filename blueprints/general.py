from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify, current_app

from config.decorators import login_required
from config.exts import db
from config.models import UserModel, SettingModel
from werkzeug.security import generate_password_hash, check_password_hash

from utils.captchas import getCaptchaPic

bp = Blueprint('general', __name__, url_prefix='/')


@bp.route('/getCaptchaImg', methods=['POST'])
def getCaptchaImg():
    file_name, coding = getCaptchaPic(request.form.get('coding'))
    return jsonify({'code': 200, 'src': file_name, 'coding': coding})


@bp.route('/Setting', methods=['GET', 'POST'])
@login_required
def Setting():
    no_pwd = 'true' if current_app.config.get('NO_PWD') else 'false'
    captcha = 'true' if current_app.config.get('CAPTCHA') else 'false'
    data = {
        'NoPwd': no_pwd,
        'Captcha': captcha
    }
    return render_template('setting.html', data=data)


@bp.route('/Change_NO_PWD', methods=['GET', 'POST'])
@login_required
def Change_NO_PWD():
    NO_PWD = request.form.get('NO_PWD')
    if NO_PWD == 'true':
        current_app.config['NO_PWD'] = True
        setting = SettingModel.query.filter_by(id=0).first()
        setting.no_pwd = 1
        db.session.commit()
    else:
        current_app.config['NO_PWD'] = False
        setting = SettingModel.query.filter_by(id=0).first()
        setting.no_pwd = 0
        db.session.commit()

    return jsonify({'code': 200, 'msg': '已修改无密码登录'})


@bp.route('/Change_CAPTCHA', methods=['GET', 'POST'])
@login_required
def Change_CAPTCHA():
    Captcha = request.form.get('CAPTCHA')
    if Captcha == 'true':
        current_app.config['CAPTCHA'] = True
        setting = SettingModel.query.filter_by(id=0).first()
        setting.captcha = 1
        db.session.commit()
    else:
        current_app.config['CAPTCHA'] = False
        setting = SettingModel.query.filter_by(id=0).first()
        setting.captcha = 0
        db.session.commit()

    return jsonify({'code': 200, 'msg': '已修改登录验证码'})

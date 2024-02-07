from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify

from config.decorators import login_required
from config.exts import db
from config.models import UserModel, ConfigModel
from werkzeug.security import generate_password_hash, check_password_hash

from utils.captchas import getCaptchaPic

bp = Blueprint('general', __name__, url_prefix='/')


@bp.route('/getCaptchaImg', methods=['POST'])
def getCaptchaImg():
    file_name, coding = getCaptchaPic(request.form.get('coding'))
    return jsonify({'code': 200, 'src': file_name, 'coding': coding})


@bp.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    configs = ConfigModel.query.filter_by(id=0).first()
    no_pwd = configs.no_pwd
    data = {'no_pwd': no_pwd}
    return render_template('setting.html', data=data)


@bp.route('/change_config_data', methods=['GET', 'POST'])
@login_required
def change_config_data():
    no_pwd = request.form.get('no_pwd')
    configs = ConfigModel.query.filter_by(id=0).first()
    if no_pwd is '1':
        configs.no_pwd = 1
    else:
        configs.no_pwd = 0

    return jsonify({'code': 200, 'msg': 'success'})
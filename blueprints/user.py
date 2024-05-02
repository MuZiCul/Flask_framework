import datetime
import random
import re
import string

from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify, current_app
from flask_mail import Message

from config.decorators import login_required
from config.exts import db, redis_client, mail
from config.models import UserModel, EmailCaptchaModel
from werkzeug.security import generate_password_hash, check_password_hash

from utils.Aescrypt import Aescrypt
from utils.captchas import getCaptchaPic

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    no_pwd = current_app.config.get('NO_PWD')
    captcha = current_app.config.get('CAPTCHA')
    if captcha:
        CaptchaPic, coding = getCaptchaPic('')
    else:
        CaptchaPic, coding = 0, 0
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        if captcha:
            captcha = request.form.get('captcha')
            if not redis_client.keys(captcha.lower()):
                error = '验证码有误'
                CaptchaPic, coding = getCaptchaPic('')
                return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=account,
                                       no_pwd=no_pwd, captcha=captcha)
        user_username = UserModel.query.filter_by(email=account).first()
        if not user_username:
            error = '账户不存在'
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=account,
                                   no_pwd=no_pwd, captcha=captcha)
        if user_username and check_password_hash(user_username.password, password):
            session['userid'] = user_username.id
            return redirect(url_for('index'))
        else:
            error = '账户或密码有误'
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=account,
                                   no_pwd=no_pwd, captcha=captcha)
    return render_template('login.html', CaptchaPic=CaptchaPic, coding=coding, no_pwd=no_pwd, captcha=captcha)


@bp.route('/no_pwd_login', methods=['GET', 'POST'])
def no_pwd_login():
    return render_template('no_pwd_login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    no_pwd = current_app.config.get('NO_PWD')
    captcha = current_app.config.get('CAPTCHA')
    if captcha:
        CaptchaPic, coding = getCaptchaPic('')
    else:
        CaptchaPic, coding = 0, 0

    if hasattr(g, 'user'):
        try:
            print(g.user.id)
            return redirect(url_for('index'))
        except Exception as e:
            session.clear()
            return render_template('login.html', CaptchaPic=CaptchaPic, coding=coding, no_pwd=no_pwd, captcha=captcha,
                                   register=1)

    if request.method == 'GET':
        return render_template('login.html', CaptchaPic=CaptchaPic, coding=coding, no_pwd=no_pwd, captcha=captcha,
                               register=1)
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        if captcha:
            captcha = request.form.get('captcha')
            if not redis_client.keys(captcha.lower()):
                error = '验证码有误！'
                CaptchaPic, coding = getCaptchaPic('')
                return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=email,
                                       no_pwd=no_pwd, captcha=captcha, register=1)
        if UserModel.query.filter_by(email=email).first():
            error = '该邮箱已注册！'
            CaptchaPic, coding = getCaptchaPic('')
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=email,
                                   no_pwd=no_pwd, captcha=captcha, register=1)
        user = UserModel(email=email, username=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        user_username = UserModel.query.filter_by(email=email).first()
        session['userid'] = user_username.id
        return redirect(url_for('index'))


# @login_required
@bp.route('/user_info', methods=['GET', 'POST'])
def user_info():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    data = UserModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
    data_list = []
    for i in data.items:
        dit = {'id': i.id,
               'username': i.username,
               'email': i.email,
               'type': i.type,
               'state': i.state,
               'create_date': str(i.create_date)[:19],
               }
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': data.total, 'data': data_list}
    return dic


# @login_required
@bp.route('/user_info_html', methods=['GET', 'POST'])
def user_info_html():
    return render_template('user_info_html.html')


@bp.route('/logoff')
def logoff():
    try:
        user = UserModel.query.filter_by(id=g.user.id).first()
        user.online = 0
        redis_client.delete(f'online_userid_{user.id}', f'user_id_{user.id}')
        db.session.commit()
    except Exception as e:
        print(e)
    finally:
        session.clear()
        flash("账号已退出！")
    return redirect(url_for('user.login'))


@bp.route('/profile_data', methods=['GET', 'POST'])
@login_required
def profile_data():
    id = g.user.id
    user = UserModel.query.filter_by(id=id).first()
    data = {'username': user.username, 'email': user.email, 'state': '在职' if user.state else '离职',
            'id': id}
    return render_template('profile.html', data=data)


@bp.route('/email_login', methods=['GET', 'POST'])
def email_login():
    email = request.form.get('email')
    if not is_valid_email(email):
        return jsonify({'code': 400, 'msg': '邮箱格式不正确'})
    getCaptchaTimeReturn = getCaptchaTime(email)
    if getCaptchaTimeReturn:
        return getCaptchaTimeReturn
    user_email = UserModel.query.filter_by(email=email).first()
    if not user_email:
        return jsonify({'code': 400, 'msg': '邮箱未注册'})
    email = email.replace(' ', '')
    session['email'] = email
    captcha = ''.join(random.sample(string.digits, 6))
    message = Message(subject='【开发者登录】验证码',
                      recipients=[email],
                      body=f'【开发者管理】您的本次验证码是：{captcha}，请勿告知任何人，本次验证码将在几秒后失效！')
    mail.send(message)
    captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
    AescryptOb = Aescrypt()
    captcha = generate_password_hash(AescryptOb.encryption(captcha))
    if captcha_model:
        captcha_model.captcha = captcha
        captcha_model.type = 1
        captcha_model.create_time = datetime.datetime.now()
        db.session.commit()
    else:
        captcha_model = EmailCaptchaModel(email=email, captcha=captcha, type=1)
        db.session.add(captcha_model)
        db.session.commit()
    return jsonify({'code': 200})


@bp.route('/check_captcha', methods=['GET', 'POST'])
def check_captcha():
    from datetime import datetime
    captcha = request.form.get('captcha')
    if 'email' not in session or not captcha:
        return render_template('no_pwd_login.html', type=1)
    captcha_model = EmailCaptchaModel.query.filter_by(email=session['email']).first()
    AescryptOb = Aescrypt()
    if not captcha_model:
        return render_template('no_pwd_login.html', error='请重新获取验证码', type=2)
    else:
        time_1 = captcha_model.create_time
        time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_1_struct = datetime.strptime(str(time_1), "%Y-%m-%d %H:%M:%S")
        time_2_struct = datetime.strptime(str(time_2), "%Y-%m-%d %H:%M:%S")
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        captcha_model.type = 0
        db.session.commit()
        data = AescryptOb.encryption(captcha)
        if total_seconds > 60:
            return render_template('no_pwd_login.html', error='验证码已过期', type=2)
        elif not check_password_hash(captcha_model.captcha, data):
            return render_template('no_pwd_login.html', error='验证码不正确', type=2)
        else:
            session['userid'] = UserModel.query.filter_by(email=session['email']).first().id
            return redirect(url_for('index'))


def getCaptchaTime(email):
    captcha_model = EmailCaptchaModel.query.filter_by(email=email).order_by(db.text('-create_time')).first()
    if captcha_model:
        time_1 = captcha_model.create_time
        time_2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_1_struct = datetime.datetime.strptime(str(time_1), "%Y-%m-%d %H:%M:%S")
        time_2_struct = datetime.datetime.strptime(str(time_2), "%Y-%m-%d %H:%M:%S")
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        if total_seconds < 60:
            return jsonify({'code': 400, 'message': '获取验证码过于频繁，请稍后再试！'})
        else:
            return False


def is_valid_email(email):
    # 邮箱的正则表达式模式
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # 使用re.match函数进行匹配
    match = re.match(pattern, email)

    if match:
        return True
    else:
        return False

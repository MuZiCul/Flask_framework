import io
import os
from PIL import Image
from flask import Flask, session, g, render_template, send_file, jsonify
from flask_migrate import Migrate
from flask_apscheduler import APScheduler

from SexImg.autoT66y import T66y
from config import config, private_config
from blueprints import user_bp, general_bp
from config.decorators import login_required
from config.exts import mail, redis_client, init_db, db

from config.models import *
from utils.captchas import delCaptcha
from utils.useronline import PollingUserOnline

app = Flask(__name__)
app.config.from_object(private_config)
# app.config.from_object(config)
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'

with app.app_context():
    # 使用自定义的初始化方法
    init_db(app)
mail.init_app(app)
scheduler = APScheduler()
scheduler.init_app(app)
redis_client.init_app(app)
migrate = Migrate(app, db)
scheduler = APScheduler()
scheduler.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(general_bp)
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), 'file')
scheduler.start()


@app.before_first_request
def before_first_request():
    delCaptcha()
    T66y()
    app.config['NO_PWD'] = SettingModel.query.filter_by(id=0).first().no_pwd
    app.config['CAPTCHA'] = SettingModel.query.filter_by(id=0).first().captcha
    app.config['DEBUG'] = SettingModel.query.filter_by(id=0).first().debug



@app.before_request
def before_request():
    debug = app.config.get('DEBUG')
    if debug:
        user_id = 1
    else:
        user_id = session.get('userid')
    g.DATABASE_DATA = 0
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            if user:
                g.user = user
            else:
                g.user = ''

        except Exception as e:
            print(e)
            g.user = ''


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


@scheduler.task('interval', id='clean', seconds=300)
def clean():
    try:
        with scheduler.app.app_context():
            delCaptcha()
            PollingUserOnline()
    finally:
        pass


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    with app.app_context():
        T66y()
    return jsonify({'code': 200})


@app.route('/console')
def console():
    return render_template('console.html')


# 定时清理验证码图片
@scheduler.task('interval', id='delCaptcha', minutes=10)
def check_net():
    try:
        with scheduler.app.app_context():
            delCaptcha()
    finally:
        pass


@scheduler.task('interval', id='delCaptcha', minutes=180)
def T66y_task():
    try:
        with scheduler.app.app_context():
            T66y()
    finally:
        pass


@app.route('/file/<name>', methods=['GET', 'POST'])
def get_file(name):
    if not os.path.exists('file/' + name):
        return 0
    with open('file/' + name, 'rb') as f:
        img = Image.open(f)

        # 将图片转换为JPEG格式
        img = img.convert('RGB')
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)

    # 返回图片文件
    return send_file(img_io, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(port=5001)

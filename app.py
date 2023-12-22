import io
import os
from PIL import Image
from flask import Flask, session, g, render_template, send_file
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from config import config, private_config
from blueprints import user_bp, general_bp
from config.decorators import login_required
from config.exts import mail, redis_client

from config.models import *
from utils.captchas import delCaptcha
from utils.useronline import PollingUserOnline

app = Flask(__name__)
app.config.from_object(private_config)
# app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
scheduler = APScheduler()
scheduler.init_app(app)
redis_client.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(user_bp)
app.register_blueprint(general_bp)
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), 'file')


@app.before_request
def before_request():
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
    app.run()

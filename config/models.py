from config.exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), default='')
    type = db.Column(db.Integer, default=0)  # -1为DEBUG账户
    state = db.Column(db.Integer, default=0)
    logout = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(100),
                     default='default_icon.png')
    create_date = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now)


class SettingModel(db.Model):
    __tablename__ = "setting"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no_pwd = db.Column(db.Integer, default=0)
    captcha = db.Column(db.Integer, default=0)
    debug = db.Column(db.Integer, default=0)


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Integer, default='1')
    create_time = db.Column(db.DateTime, default=datetime.now)


class SpuModel(db.Model):
    __tablename__ = 'spu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), default='')
    title = db.Column(db.String(255), default='')
    kind = db.Column(db.String(255), default='')
    quality = db.Column(db.String(255), default='')
    all_size = db.Column(db.String(255), default='')
    avg_size = db.Column(db.String(255), default='')
    publish_date = db.Column(db.String(255), default='')
    img_size = db.Column(db.String(255), default='')
    pcImg = db.Column(db.String(255), default='')
    phoneImg = db.Column(db.String(255), default='')
    dir = db.Column(db.String(255), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Spu {self.title}>'


class FpuModel(db.Model):
    __tablename__ = 'fpu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), default='')
    title = db.Column(db.String(255), default='')
    publish_date = db.Column(db.String(255), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)
    reason = db.Column(db.String(255), default='')

    def __repr__(self):
        return f'<Fpu {self.title}>'


class LogModel(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.String(255), default='')
    content = db.Column(db.String(2000), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Log {self.content}>'


class ConfigModel(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255), default='')
    key = db.Column(db.String(255), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)



class JpuModel(db.Model):
    __tablename__ = 'jpu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), default='')
    title = db.Column(db.String(255), default='')
    reason = db.Column(db.String(255), default='')
    publish_date = db.Column(db.String(255), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Jpu {self.title}>'


class FiuModel(db.Model):
    __tablename__ = 'fiu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.String(255), default='')
    url = db.Column(db.String(255), default='')
    title = db.Column(db.String(255), default='')
    reason = db.Column(db.String(255), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Fiu {self.title}>'


class SiuModel(db.Model):
    __tablename__ = 'siu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.String(255), default='')
    url = db.Column(db.String(255), default='')
    title = db.Column(db.String(255), default='')
    size = db.Column(db.String(255), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Siu {self.title}>'


class AgainpageModel(db.Model):
    __tablename__ = 'againpage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.Integer, default=0)
    url = db.Column(db.String(255), default='')
    title = db.Column(db.String(255), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)
    count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Againpage {self.state}>'


class ReFiuModel(db.Model):
    __tablename__ = 're_fiu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200), default='')
    title = db.Column(db.String(200), default='')
    state = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<ReFiu {self.state}>'




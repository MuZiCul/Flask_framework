from config.exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), default='')
    type = db.Column(db.Integer, default=0)
    state = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(100),
                     default='default_icon.png')
    create_date = db.Column(db.DateTime, default=datetime.now)


class ConfigModel(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no_pwd = db.Column(db.Integer, default=0)


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Integer, default='1')
    create_time = db.Column(db.DateTime, default=datetime.now)



